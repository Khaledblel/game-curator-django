document.addEventListener('DOMContentLoaded', function() {
  // Initialize stickers for the hero section (section 1)
  initStickers('hero-sticker-container', 15); // More stickers in section 1
  
  // Initialize stickers for the CTA section (section 3)
  initStickers('cta-sticker-container', 6); // Fewer stickers in section 3
});

function initStickers(containerId, count) {
  const container = document.getElementById(containerId);
  if (!container) return;
  
  // Clear any existing stickers
  container.innerHTML = '';
  
  // Divide container into grid sections to ensure even distribution
  const gridCols = Math.ceil(Math.sqrt(count));
  const gridRows = Math.ceil(count / gridCols);
  const cellWidth = container.offsetWidth / gridCols;
  const cellHeight = container.offsetHeight / gridRows;
  
  // Keep track of placed stickers to prevent overlapping
  const placedStickers = [];
  const minDistance = 120; // Minimum distance between stickers
  
  // Create stickers
  for (let i = 1; i <= count; i++) {
    const sticker = document.createElement('img');
    sticker.className = 'sticker';
    
    // Get a random sticker image (updated to use sticker_01 to sticker_34)
    const stickerNumber = Math.floor(Math.random() * 34) + 1;
    const paddedNumber = stickerNumber.toString().padStart(2, '0');
    sticker.src = `/static/recommender/assets/stickers/sticker_${paddedNumber}.png`;
    
    // Determine which grid cell this sticker belongs to
    const cellRow = Math.floor((i-1) / gridCols);
    const cellCol = (i-1) % gridCols;
    
    // Set position within the cell with padding from edges
    const padding = 40;
    const maxAttempts = 10;
    
    let posX, posY;
    let attempt = 0;
    let validPosition = false;
    
    while (attempt < maxAttempts && !validPosition) {
      // Calculate position within the cell
      posX = cellCol * cellWidth + padding + Math.random() * (cellWidth - 2 * padding);
      posY = cellRow * cellHeight + padding + Math.random() * (cellHeight - 2 * padding);
      
      // Check if this position is far enough from other stickers
      validPosition = true;
      for (let j = 0; j < placedStickers.length; j++) {
        const existingSticker = placedStickers[j];
        const distance = Math.sqrt(
          Math.pow(posX - existingSticker.x, 2) + 
          Math.pow(posY - existingSticker.y, 2)
        );
        
        if (distance < minDistance) {
          validPosition = false;
          break;
        }
      }
      
      attempt++;
    }
    
    // Place sticker
    sticker.style.left = `${posX}px`;
    sticker.style.top = `${posY}px`;
    
    // Add to list of placed stickers
    placedStickers.push({ x: posX, y: posY });
    
    container.appendChild(sticker);
  }
}