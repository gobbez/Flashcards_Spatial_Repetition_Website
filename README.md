# Spatial Repetition Website

A modern Italian/English website for spaced repetition training. Users can upload a simple text file containing flashcards, and the application will help them study using a custom spaced repetition algorithm.

## Features
- **File Upload**: Supports `.txt` files with a specific `F: / B:` format.
- **Spaced Repetition Algorithm**: 
  - "Understood" -> Re-appears at ~90% of the queue.
  - "So and So" -> Re-appears at ~30% of the queue.
  - "Study More" -> Re-appears at ~10% of the queue.
- **Modern UI**: Glassmorphism design, dark mode, and smooth transitions.

## How to Use

1. **Prepare your flashcards**: Create a `.txt` file with the following format:
   ```
   F: "Front of the card"
   B: "Back of the card"
   F: "Pizza"
   B: "Delicious Italian food"
   ```
2. **Upload**: Open the website and drag & drop your file.
3. **Study**: 
   - Click "Start Studying".
   - Review the front of the card.
   - Click "Show Back" to reveal the answer.
   - Rate your understanding ("Understood", "So and so", "Study more") to schedule the card's next appearance.

## Project Setup

```sh
npm install
```

### Compile and Hot-Reload for Development

```sh
npm run dev
```

### Build for Production

```sh
npm run build
```

## License

This project is open for use but requires attribution.
**You must quote the original author upon use.**

© 2026 Spatial Repetition Website 
