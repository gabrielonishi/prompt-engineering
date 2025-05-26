// Initialize canvas and context
const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');
const startBtn = document.getElementById('startBtn');
const scoreElement = document.getElementById('score');

// Game settings
const bgMusic = document.getElementById('bgMusic');
const gridSize = 20; // Size of each grid cell (snake segment/food)
let snake = [];
let food = {};
let dx = gridSize; // Horizontal velocity (starts moving right)
let dy = 0; // Vertical velocity
let score = 0;
let gameSpeed = 150; // Initial delay between moves (ms)
let gameLoop;
let highScore = 0;
let pinkFood = null; // Stores pink block position
let pinkFoodTimer = null; // For despawning
const PINK_SPAWN_INTERVAL = { min: 5000, max: 15000 }; // Spawn every 5-15s

// Add to game.js variables
let nextDx = gridSize; // Buffer for queued direction
let nextDy = 0;

let isPaused = false;
const pauseBtn = document.getElementById('pauseBtn');
const pausedOverlay = document.createElement('div');
pausedOverlay.className = 'paused-overlay';
pausedOverlay.textContent = 'PAUSED';
document.body.appendChild(pausedOverlay);

// Pause button click handler
pauseBtn.addEventListener('click', () => {
  if (!gameLoop) return; // Disable if game isn't running

  isPaused = !isPaused;
  pauseBtn.textContent = isPaused ? 'Resume' : 'Pause';
  pausedOverlay.style.display = isPaused ? 'block' : 'none';

  if (isPaused) {
    clearInterval(gameLoop);
    bgMusic.pause();

  } else {
    gameLoop = setInterval(moveSnake, gameSpeed);
    bgMusic.play();
  }
});

// Event Listeners
startBtn.addEventListener('click', initGame);

function initGame() {
  // Clear pink food
  pinkFood = null;
  clearTimeout(pinkFoodTimer);
  
  isPaused = false;
  pauseBtn.textContent = 'Pause';
  pausedOverlay.style.display = 'none';
  
  snake = [
    { x: 5 * gridSize, y: 5 * gridSize },
    { x: 4 * gridSize, y: 5 * gridSize },
    { x: 3 * gridSize, y: 5 * gridSize }
  ];

    // Reset and play music
  bgMusic.currentTime = 0; // Restart song
  bgMusic.play().catch(() => {}); // Mute autoplay errors
  
  // Reset direction AND buffer
  dx = gridSize;
  dy = 0;
  nextDx = dx;
  nextDy = dy;
  gameSpeed = 150; // Initial delay between moves (ms)

  
  scoreElement.textContent = `Score: ${score}`;
  
  // Clear previous game loop (if any)
  if (gameLoop) clearInterval(gameLoop);
  
  // Spawn first food
  createFood();
  
  // Start game loop
  gameLoop = setInterval(moveSnake, gameSpeed);
}

function trySpawnPinkFood() {
  // Only spawn if no existing pink food
  if (!pinkFood) {
    pinkFood = {
      x: Math.floor(Math.random() * (canvas.width / gridSize)) * gridSize,
      y: Math.floor(Math.random() * (canvas.height / gridSize)) * gridSize
    };

    // Ensure it doesn’t overlap snake or normal food
    const overlaps = [...snake, food].some(item => 
      item.x === pinkFood.x && item.y === pinkFood.y
    );
    
    if (overlaps) {
      pinkFood = null;
      return;
    }

    // Despawn after 3 seconds
    pinkFoodTimer = setTimeout(() => {
      pinkFood = null;
    }, 3000);
  }
}

// Start periodic spawn attempts
setInterval(trySpawnPinkFood, Math.random() * (PINK_SPAWN_INTERVAL.max - PINK_SPAWN_INTERVAL.min) + PINK_SPAWN_INTERVAL.min);

function createFood() {
  // Generate random grid-aligned position
  food = {
    x: Math.floor(Math.random() * (canvas.width / gridSize)) * gridSize,
    y: Math.floor(Math.random() * (canvas.height / gridSize)) * gridSize
  };

  // Ensure food doesn’t spawn on the snake
  snake.forEach(segment => {
    if (segment.x === food.x && segment.y === food.y) {
      createFood(); // Retry recursively
    }
  });
}

function checkWallCollision(head) {
  return (
    head.x < 0 || 
    head.x >= canvas.width || 
    head.y < 0 || 
    head.y >= canvas.height
  );
}

function checkSelfCollision(head) {
  return snake.some((segment, index) => {
    // Skip checking the head against itself
    if (index === 0) return false;
    return segment.x === head.x && segment.y === head.y;
  });
}

function moveSnake() {
  // Create new head position
  dx = nextDx;
  dy = nextDy;

  const head = { 
    x: snake[0].x + dx, 
    y: snake[0].y + dy 
  };
  // Check collisions
  if (checkWallCollision(head) || checkSelfCollision(head)) {
    gameOver();
    return;
  }

  if (pinkFood && head.x === pinkFood.x && head.y === pinkFood.y) {
    score += 20; // Bonus points
    scoreElement.textContent = `Score: ${score}`;
    
    // Slow down game (reverse normal speed gain)
    gameSpeed *= 1.05; 
    clearInterval(gameLoop);
    gameLoop = setInterval(moveSnake, gameSpeed);
    
    clearTimeout(pinkFoodTimer); // Cancel despawn timer
    pinkFood = null;
  }

  // Add new head to snake
  snake.unshift(head);

  if (head.x === food.x && head.y === food.y) {
    score += 10;
    scoreElement.textContent = `Score: ${score}`;
    
    // Speed up game
    gameSpeed *= 0.95; // Adjust multiplier for desired difficulty
    clearInterval(gameLoop);
    gameLoop = setInterval(moveSnake, gameSpeed);
    
    createFood();
  } else {
    snake.pop();
  }

  // Reset buffer to current direction (prevent queued turns)
  nextDx = dx;
  nextDy = dy;
  
  draw();

}

function gameOver() {
  clearInterval(gameLoop);
  bgMusic.pause();

  if (score > highScore) {
    highScore = score;
    localStorage.setItem('snakeHighScore', highScore);
    document.getElementById('highScore').textContent = `High Score: ${highScore}`;
  }
  
  alert(`Game Over! Score: ${score}. High Score: ${highScore}`);
  initGame();
}

function draw() {
  // Clear canvas
  ctx.fillStyle = '#34495e';
  ctx.fillRect(0, 0, canvas.width, canvas.height);

  // Draw snake
  snake.forEach((segment, index) => {
    ctx.fillStyle = index === 0 ? '#e74c3c' : '#2ecc71'; // Red head, green body
    ctx.fillRect(segment.x, segment.y, gridSize - 2, gridSize - 2); // Slight gap between segments
  });

  // Draw food
  ctx.fillStyle = '#f1c40f';
  ctx.fillRect(food.x, food.y, gridSize - 2, gridSize - 2);

  if (pinkFood) {
    ctx.fillStyle = '#ff69b4'; // Pink color
    ctx.fillRect(pinkFood.x, pinkFood.y, gridSize - 2, gridSize - 2);
  }
}

document.addEventListener('keydown', (e) => {
  const keyPressed = e.key;
  const currentDx = dx; // Use ACTUAL current direction for validation
  const currentDy = dy;

  // Prevent 180-degree turns using CURRENT direction
  if (keyPressed === 'ArrowUp' && currentDy !== gridSize) {
    nextDx = 0;
    nextDy = -gridSize;
  } else if (keyPressed === 'ArrowDown' && currentDy !== -gridSize) {
    nextDx = 0;
    nextDy = gridSize;
  } else if (keyPressed === 'ArrowLeft' && currentDx !== gridSize) {
    nextDx = -gridSize;
    nextDy = 0;
  } else if (keyPressed === 'ArrowRight' && currentDx !== -gridSize) {
    nextDx = gridSize;
    nextDy = 0;
  }
});

// Initialize high score from localStorage
if (localStorage.getItem('snakeHighScore')) {
  highScore = parseInt(localStorage.getItem('snakeHighScore'));
  document.getElementById('highScore').textContent = `High Score: ${highScore}`;
}

