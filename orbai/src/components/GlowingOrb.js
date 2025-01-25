import React from "react";
import { Canvas } from "@react-three/fiber";
import { Sphere, MeshWobbleMaterial } from "@react-three/drei";

const GlowingOrb = ({ volume }) => {
  const glowColor = volume > 0.2 ? "#ff5555" : "#00ffff"; // Change color based on volume
  const wobbleIntensity = Math.min(1 + volume * 5, 2); // Adjust wobble based on volume

  return (
    <Canvas>
      <ambientLight intensity={0.5} />
      <pointLight position={[10, 10, 10]} />
      <Sphere args={[1, 32, 32]}>
        <MeshWobbleMaterial
          color={glowColor}
          speed={wobbleIntensity}
          factor={volume * 2} // Intensity of wobble
        />
      </Sphere>
    </Canvas>
  );
};

export default GlowingOrb;
