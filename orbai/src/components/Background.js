import { useEffect } from "react"; // Remove 'React' if not used
import { gsap } from "gsap";

const Background = () => {
  useEffect(() => {
    const gradientColors = {
      color1: "#2e0066",
      color2: "#00ffcc",
    };

    gsap.to(gradientColors, {
      color1: "#ff00ff",
      color2: "#00ffff",
      duration: 4,
      repeat: -1,
      yoyo: true,
      onUpdate: () => {
        document.body.style.background = `radial-gradient(circle, ${gradientColors.color1}, ${gradientColors.color2})`;
      },
    });
  }, []);

  return null;
};

export default Background;
