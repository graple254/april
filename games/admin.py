# project_folder/your_app_name/admin.py

from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext as _
from .models import *

@admin.register(SudokuPuzzle)
class SudokuPuzzleAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_difficulty_display_with_clues', 'created_at_formatted', 'preview_initial_board')
    list_filter = ('difficulty', 'clues')
    search_fields = ('id',)
    readonly_fields = ('created_at',)

    fieldsets = (
        (None, {
            'fields': ('difficulty', 'clues')
        }),
        ('Puzzle Data (9x9 Grid)', {
            'classes': ('collapse',), # Collapsible section
            'fields': ('initial_board', 'solution'),
            'description': _("Grids are 9x9 lists of lists (0 for empty). Edit with caution.")
        }),
        ('Timestamps', {
            'fields': ('created_at',),
        }),
    )

    def get_difficulty_display_with_clues(self, obj):
        return f"{obj.get_difficulty_display()} ({obj.clues} clues)"
    get_difficulty_display_with_clues.short_description = _("Type")
    get_difficulty_display_with_clues.admin_order_field = 'difficulty'

    def created_at_formatted(self,obj):
        return obj.created_at.strftime("%d-%m-%Y %H:%M")
    created_at_formatted.short_description = _("Created")
    created_at_formatted.admin_order_field = 'created_at'

    def preview_initial_board(self, obj):
        if obj.initial_board and isinstance(obj.initial_board, list) and len(obj.initial_board) > 0:
            return str(obj.initial_board[0]) + "..." # Preview first row
        return "N/A"
    preview_initial_board.short_description = _("Board Preview")

@admin.register(GameSession)
class GameSessionAdmin(admin.ModelAdmin):
    list_display = (
        'get_short_session_id', 'player1_display', 'player2_display', 
        'status', 'winner_display', 'puzzle_id_display', 'created_at_formatted', 'started_at_formatted'
    )
    list_filter = ('status', 'sudoku_puzzle__difficulty', 'created_at', 'started_at')
    search_fields = ('session_id__iexact', 'player1__username__iexact', 'player2__username__iexact')
    
    readonly_fields = (
        'session_id', 'created_at', 'started_at', 'ended_at', 
        'player1_board_admin_display', 'player2_board_admin_display'
    )
    
    fieldsets = (
        (_('Session Overview'), {
            'fields': ('session_id', 'status', 'sudoku_puzzle')
        }),
        (_('Player Details'), {
            'fields': (
                ('player1', 'player1_incorrect_strikes', 'player1_correct_cells_count'),
                ('player2', 'player2_incorrect_strikes', 'player2_correct_cells_count'),
                'winner'
            )
        }),
        (_('Game Boards (Read-only Preview)'), {
            'classes': ('collapse',),
            'fields': ('player1_board_admin_display', 'player2_board_admin_display'),
            'description': _("Current state of player boards. Not directly editable here.")
        }),
        (_('Timestamps'), {
            'fields': ('created_at', 'started_at', 'ended_at')
        }),
    )

    def get_short_session_id(self, obj):
        return str(obj.session_id)[:8]
    get_short_session_id.short_description = _("Session ID")

    def player1_display(self, obj):
        return obj.player1.username if obj.player1 else "---"
    player1_display.short_description = _("Player 1")
    player1_display.admin_order_field = 'player1__username'

    def player2_display(self, obj):
        return obj.player2.username if obj.player2 else _("Waiting...")
    player2_display.short_description = _("Player 2")
    player2_display.admin_order_field = 'player2__username'

    def winner_display(self, obj):
        return obj.winner.username if obj.winner else "---"
    winner_display.short_description = _("Winner")
    winner_display.admin_order_field = 'winner__username'

    def puzzle_id_display(self, obj):
        return obj.sudoku_puzzle.id if obj.sudoku_puzzle else "---"
    puzzle_id_display.short_description = _("Puzzle ID")
    puzzle_id_display.admin_order_field = 'sudoku_puzzle__id'
    
    def created_at_formatted(self, obj):
        return obj.created_at.strftime("%d-%m-%Y %H:%M") if obj.created_at else "---"
    created_at_formatted.short_description = _("Created")
    created_at_formatted.admin_order_field = 'created_at'

    def started_at_formatted(self, obj):
        return obj.started_at.strftime("%d-%m-%Y %H:%M") if obj.started_at else "---"
    started_at_formatted.short_description = _("Started")
    started_at_formatted.admin_order_field = 'started_at'

    def _format_board_html(self, board_data):
        if not board_data or not isinstance(board_data, list):
            return _("Not available or invalid board format.")
        
        html_board = "<table style='border-collapse: collapse; font-family: monospace; margin: 5px 0;'>"
        for i, row in enumerate(board_data):
            if i > 0 and i % 3 == 0:
                html_board += "<tr><td colspan='9' style='height:2px; background-color:#999;'></td></tr>"
            html_board += "<tr>"
            if not isinstance(row, list) or len(row) != 9:
                return _("Invalid row format in board data.")
            for j, cell in enumerate(row):
                style = "border: 1px solid #ccc; padding: 3px 5px; text-align: center; min-width: 22px; height:22px;"
                if j > 0 and j % 3 == 0:
                     style += "border-left: 2px solid #999;"
                display_val = str(cell) if cell != 0 else "."
                html_board += f"<td style='{style}'>{display_val}</td>"
            html_board += "</tr>"
        html_board += "</table>"
        return format_html(html_board)

    def player1_board_admin_display(self, obj):
        return self._format_board_html(obj.player1_current_board)
    player1_board_admin_display.short_description = _("P1 Board")

    def player2_board_admin_display(self, obj):
        return self._format_board_html(obj.player2_current_board)
    player2_board_admin_display.short_description = _("P2 Board")