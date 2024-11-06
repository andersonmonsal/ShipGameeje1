document.addEventListener('DOMContentLoaded', function() {
    const gameBoard = document.getElementById('game-board');
    const attackButton = document.getElementById('attack-button');
    
    function createBoard(board, isAttackBoard = false) {
        if (!gameBoard) return;
        
        gameBoard.innerHTML = '';
        const letters = 'ABCDE';
        
        // Crear cabecera de columnas
        const headerRow = document.createElement('div');
        headerRow.className = 'board-row';
        headerRow.innerHTML = '<div class="cell"></div>' + 
            letters.split('').map(letter => 
                `<div class="cell">${letter}</div>`
            ).join('');
        gameBoard.appendChild(headerRow);
        
        // Crear filas del tablero
        board.forEach((row, i) => {
            const boardRow = document.createElement('div');
            boardRow.className = 'board-row';
            
            // Número de fila
            const rowNumber = document.createElement('div');
            rowNumber.className = 'cell';
            rowNumber.textContent = i + 1;
            boardRow.appendChild(rowNumber);
            
            // Células del tablero
            row.forEach((cell, j) => {
                const cellDiv = document.createElement('div');
                cellDiv.className = 'cell';
                cellDiv.dataset.row = i;
                cellDiv.dataset.col = j;
                
                // Asignar clase según el estado de la célula
                if (cell === 1 && !isAttackBoard) cellDiv.classList.add('ship');
                if (cell === 2) cellDiv.classList.add('hit');
                if (cell === -1) cellDiv.classList.add('miss');
                
                cellDiv.addEventListener('click', () => handleCellClick(i, j));
                boardRow.appendChild(cellDiv);
            });
            
            gameBoard.appendChild(boardRow);
        });
    }
    
    function handleCellClick(row, col) {
        const letter = String.fromCharCode(65 + col);
        const position = `${letter}${row + 1}`;
        
        // Si estamos en fase de colocación de barcos
        if (!gameStarted) {
            fetch('/place_ship', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: `position=${position}`
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    updateBoard();
                }
            });
        } else { // Si estamos en fase de ataque
            fetch('/shoot', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: `position=${position}`
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    updateBoard();
                    if (data.game_over) {
                        alert(`¡Juego terminado! Ganador: ${data.winner}`);
                        window.location.href = '/game';
                    }
                }
            });
        }
    }
    
    function updateBoard() {
        fetch('/get_board')
            .then(response => response.json())
            .then(data => {
                if (data.board) {
                    createBoard(data.board, false);
                    createBoard(data.board_attack, true);
                }
            });
    }
    
    // Actualizar el tablero inicialmente
    if (gameBoard) {
        updateBoard();
    }
});