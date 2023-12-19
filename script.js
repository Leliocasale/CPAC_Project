//valori energia istantanea
// Carica il file JSON
import { data } from './data.js';
const { values } = data;
const canvas = document.getElementById('canvas1');
const playBtn = document.getElementById('play');
const player = document.getElementById('player');

playBtn.addEventListener('click', () => {
  player.play(); 
});

const ctx = canvas.getContext('2d');
canvas.width = 1500;
canvas.height = 800;

// canvas settings
ctx.fillStyle = "white";
ctx.strokeStyle = "white";
ctx.lineWidth = 1; // dimension of the line

class Particle {
    constructor(effect) {
        this.effect = effect;
        this.x = Math.floor(Math.random() * this.effect.width);
        this.y = Math.floor(Math.random() * this.effect.height);
        this.speedX; // 1 pixel per frame
        this.speedY;
        this.speedModifier = Math.floor(Math.random() * 2 + 1); // velocità vermicelli

        this.history = [{x: this.x, y: this.y}];
        this.maxLength = Math.floor(Math.random() * 60 + 50); // lunghezza vermicelli
        this.angle = 0;
        this.newAngle = 0;
        this.angleCorrector = Math.random() * 0.5 + 0.01;
        this.timer = this.maxLength * 2; // tempo di vita vermicelli
        this.colors = ['#e01433', '#a82222', '#a60707', '#e01433', '#e01433'];
        this.color = this.colors[Math.floor(Math.random() * this.colors.length)]; 
    }

    draw(context) {
        context.beginPath();
        context.moveTo(this.history[0].x, this.history[0].y);
        for (let i = 0; i < this.history.length; i++) {
            context.lineTo(this.history[i].x, this.history[i].y);
        }
        context.strokeStyle = this.color;
        context.stroke();
    }

    update(energy) {
        this.timer--;
        if (this.timer >= 1){
            let x = Math.floor(this.x / this.effect.cellSize);
            let y = Math.floor(this.y / this.effect.cellSize);
            let index = y * this.effect.cols + x;

            if (this.effect.flowField[index]) {
                this.newAngle = this.effect.flowField[index].colorAngle;
                if (this.angle > this.newAngle) {
                    this.angle -= this.angleCorrector;
                } else if (this.angle < this.newAngle) {
                    this.angle += this.angleCorrector;
                } else {
                    this.angle = this.newAngle;
                }
            }

            this.speedX = Math.cos(this.angle);
            this.speedY = Math.sin(this.angle);
            this.x += this.speedX * this.speedModifier;
            this.y += this.speedY * this.speedModifier;
        
            this.history.push({x: this.x, y: this.y});
            if (this.history.length > this.maxLength) {
                this.history.shift();
            }
        } else if (this.history.length > 1) {
            this.history.shift();
        } else {
            this.reset();
        }
        
    }

    reset() {
        let attempts = 0;
        let resetSuccess = false;

        while (attempts < 4 && !resetSuccess) {
            attempts++;
            let testIndex = Math.floor(Math.random() * this.effect.flowField.length);
            if (this.effect.flowField[testIndex].alpha > 0) {
                this.x = this.effect.flowField[testIndex].x;
                this.y = this.effect.flowField[testIndex].y;
                this.history = [{x: this.x, y: this.y}];
                this.timer = this.maxLength * 2;
                resetSuccess = true;
            }
        }
        
        if (!resetSuccess) {
            this.x = Math.random() * this.effect.width;
            this.y = Math.random() * this.effect.height;
            // this.history = [{x: this.x, y: this.y}];
            // this.timer = this.maxLength * 2;
        }

        
    }
}

// Array per memorizzare le particelle 
const particles = [];

// Indice per scorrere i valori di energia
let energyIndex = 0;

// Main loop
function loop() {

  // Aggiorna posizione particelle in base a energia istantanea
  particles.forEach(p => {
    p.update(values[energyIndex]);
  });
  
  // Disegna particelle
  particles.forEach(p => {
    p.draw(); 
  });

  energyIndex++;
  requestAnimationFrame(loop);

}

// Avvia!
loop();
