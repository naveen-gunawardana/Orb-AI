import React, { useEffect, useRef } from "react";

const GalaxyBackground = () => {
    const canvasRef = useRef(null);

    useEffect(() => {
        const canvas = canvasRef.current;
        const ctx = canvas.getContext("2d");
        const { innerWidth, innerHeight } = window;

        canvas.width = innerWidth;
        canvas.height = innerHeight;

        const stars = [];
        const numStars = 500;

        // Create stars
        for (let i = 0; i < numStars; i++) {
            stars.push({
                x: Math.random() * innerWidth,
                y: Math.random() * innerHeight,
                radius: Math.random() * 1.5,
                opacity: Math.random(), // Initial opacity
                flickerSpeed: Math.random() * 0.02 + 0.005, // Random flicker speed
            });
        }

        // Draw stars
        const drawStars = () => {
            ctx.clearRect(0, 0, innerWidth, innerHeight);
            stars.forEach((star) => {
                ctx.beginPath();
                ctx.arc(star.x, star.y, star.radius, 0, Math.PI * 2);
                ctx.fillStyle = `rgba(255, 255, 255, ${star.opacity})`;
                ctx.fill();
            });
        };

        // Animate stars
        const animate = () => {
            stars.forEach((star) => {
                star.opacity += star.flickerSpeed;
                if (star.opacity >= 1 || star.opacity <= 0) {
                    star.flickerSpeed *= -1; // Reverse the direction of flicker
                }
            });

            drawStars();
            requestAnimationFrame(animate);
        };

        animate();

        // Handle resizing
        const handleResize = () => {
            canvas.width = window.innerWidth;
            canvas.height = window.innerHeight;
            stars.forEach((star) => {
                star.x = Math.random() * window.innerWidth;
                star.y = Math.random() * window.innerHeight;
                star.radius = Math.random() * 1.5;
                star.opacity = Math.random();
                star.flickerSpeed = Math.random() * 0.02 + 0.005;
            });
        };

        window.addEventListener("resize", handleResize);

        return () => window.removeEventListener("resize", handleResize);
    }, []);

    return <canvas ref={canvasRef}></canvas>;
};

export default GalaxyBackground;
