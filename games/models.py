import uuid
from django.db import models
from django.contrib.auth.models import User # Using Django's built-in User model for MVP
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

class SudokuPuzzle(models.Model):
    """
    Stores a Sudoku puzzle's initial state, solution, and attributes.
    For the MVP, we assume puzzles are pre-generated or added via admin.
    """
    class Difficulty(models.TextChoices):
        # As per previous discussions, only "Extreme" is the focus for the game mode.
        # This field is kept for potential future puzzle categorization.
        EXTREME = 'EXTREME', _('Extreme') 
        # Add other difficulties here if the game later supports them.

    initial_board = models.JSONField(
        help_text=_("A 9x9 grid (list of lists) representing the initial puzzle. 0 for empty cells.")
    )
    solution = models.JSONField(
        help_text=_("A 9x9 grid (list of lists) representing the solution.")
    )
    difficulty = models.CharField(
        max_length=20,
        choices=Difficulty.choices,
        default=Difficulty.EXTREME,
        help_text=_("Difficulty category of the puzzle itself.")
    )
    clues = models.PositiveSmallIntegerField(
        default=25, # Default for "Extreme" as per previous context
        help_text=_("Number of pre-filled cells in the puzzle.")
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Puzzle {self.id} ({self.get_difficulty_display()} - {self.clues} clues)"

    class Meta:
        ordering = ['-created_at']
        verbose_name = _("Sudoku Puzzle")
        verbose_name_plural = _("Sudoku Puzzles")

class GameSession(models.Model):
    """
    Represents a Sudoku game session between two players.
    """
    class GameStatus(models.TextChoices):
        WAITING_FOR_PLAYER = 'WAITING', _('Waiting for Player 2')
        ACTIVE = 'ACTIVE', _('Active')
        PLAYER1_WON = 'P1_WON', _('Player 1 Won')
        PLAYER2_WON = 'P2_WON', _('Player 2 Won')
        # DRAW = 'DRAW', _('Draw') # Future consideration
        FORFEIT_P1_STRIKES = 'P1_STRIKES', _('Player 1 Forfeited (Max Strikes)')
        FORFEIT_P2_STRIKES = 'P2_STRIKES', _('Player 2 Forfeited (Max Strikes)')
        # Add other statuses like P1_DISCONNECTED, P2_DISCONNECTED later

    session_id = models.UUIDField(
        default=uuid.uuid4, 
        editable=False, 
        unique=True, 
        help_text=_("Unique ID for the game session/room (can be used for invites).")
    )
    
    sudoku_puzzle = models.ForeignKey(
        SudokuPuzzle, 
        on_delete=models.PROTECT, # Prevent puzzle deletion if games are using it
        related_name="game_sessions"
    )
    
    player1 = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, # Keep game record if user is deleted
        null=True, 
        related_name="game_sessions_as_player1",
        help_text=_("The user who initiated the game.")
    )
    player2 = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, # Player 2 can be null until they join
        related_name="game_sessions_as_player2",
        help_text=_("The user who joined the game.")
    )

    # Stores the current state of each player's board attempts (list of 9 lists of ints)
    player1_current_board = models.JSONField(
        null=True, blank=True, help_text=_("Player 1's current Sudoku board state.")
    )
    player2_current_board = models.JSONField(
        null=True, blank=True, help_text=_("Player 2's current Sudoku board state.")
    )

    player1_incorrect_strikes = models.PositiveSmallIntegerField(
        default=0, help_text=_("Number of incorrect moves made by Player 1.")
    )
    player2_incorrect_strikes = models.PositiveSmallIntegerField(
        default=0, help_text=_("Number of incorrect moves made by Player 2.")
    )

    # Tracks number of unique cells correctly filled by each player (beyond prefilled)
    player1_correct_cells_count = models.PositiveSmallIntegerField(default=0)
    player2_correct_cells_count = models.PositiveSmallIntegerField(default=0)

    status = models.CharField(
        max_length=20,
        choices=GameStatus.choices,
        default=GameStatus.WAITING_FOR_PLAYER,
    )
    winner = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, blank=True, 
        related_name="sudoku_games_won"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    started_at = models.DateTimeField(null=True, blank=True, help_text=_("Timestamp when Player 2 joins and game becomes active."))
    ended_at = models.DateTimeField(null=True, blank=True, help_text=_("Timestamp when the game concludes."))

    def __str__(self):
        p1_name = self.player1.username if self.player1 else "Player 1"
        p2_name = self.player2.username if self.player2 else "Waiting..."
        return f"Game {str(self.session_id)[:8]}: {p1_name} vs {p2_name} [{self.get_status_display()}]"

    def save(self, *args, **kwargs):
        is_new = not self.pk
        old_instance = None
        if not is_new:
            try:
                old_instance = GameSession.objects.get(pk=self.pk)
            except GameSession.DoesNotExist:
                pass # Should not happen if self.pk exists

        super().save(*args, **kwargs) # Save first

        if is_new and self.sudoku_puzzle and self.player1:
            # Initialize player1's board when a new game is created by player1
            if not self.player1_current_board:
                self.player1_current_board = self.sudoku_puzzle.initial_board
                super().save(update_fields=['player1_current_board'])

        # When player2 joins and game was waiting
        if old_instance and old_instance.player2 is None and self.player2 is not None and self.sudoku_puzzle:
            if self.status == self.GameStatus.WAITING_FOR_PLAYER:
                self.player2_current_board = self.sudoku_puzzle.initial_board
                self.status = self.GameStatus.ACTIVE
                self.started_at = timezone.now()
                super().save(update_fields=['player2_current_board', 'status', 'started_at'])
        
        # If game is just starting (e.g. player2 joined and status is now active)
        elif is_new and self.player1 and self.player2 and self.status == self.GameStatus.WAITING_FOR_PLAYER and self.sudoku_puzzle:
            self.player2_current_board = self.sudoku_puzzle.initial_board
            self.status = self.GameStatus.ACTIVE
            self.started_at = timezone.now()
            super().save(update_fields=['player2_current_board', 'status', 'started_at'])


    class Meta:
        ordering = ['-created_at']
        verbose_name = _("Game Session")
        verbose_name_plural = _("Game Sessions")