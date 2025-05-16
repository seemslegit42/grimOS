
/**
 * A background component that adds subtle cyberpunk-themed motifs
 * This creates a digital grid and faint circuit traces that enhance the glassmorphic effect
 */
export function CyberpunkBackground() {
  return (
    <div className="fixed inset-0 -z-10 overflow-hidden">
      {/* Near Black background as specified in the design doc (#121212) */}
      <div className="absolute inset-0 bg-[#121212]"></div>
      
      {/* Digital grid - very subtle */}
      <div 
        className="absolute inset-0 opacity-[0.07]"
        style={{
          backgroundImage: `
            linear-gradient(rgba(126, 211, 33, 0.2) 1px, transparent 1px),
            linear-gradient(90deg, rgba(126, 211, 33, 0.2) 1px, transparent 1px)
          `,
          backgroundSize: '40px 40px',
          backgroundPosition: '-1px -1px'
        }}
      ></div>
      
      {/* Circuit traces - very faint */}
      <div className="absolute inset-0 opacity-[0.05]">
        {/* Horizontal traces */}
        <div className="absolute h-[1px] w-[30%] bg-[#00BFFF] top-[20%] left-0"></div>
        <div className="absolute h-[1px] w-[20%] bg-[#00BFFF] top-[20%] right-0"></div>
        <div className="absolute h-[1px] w-[40%] bg-[#7ED321] top-[40%] right-[10%]"></div>
        <div className="absolute h-[1px] w-[35%] bg-[#FF1D58] top-[60%] left-[5%]"></div>
        <div className="absolute h-[1px] w-[25%] bg-[#00BFFF] top-[80%] right-[15%]"></div>
        
        {/* Vertical traces */}
        <div className="absolute w-[1px] h-[25%] bg-[#7ED321] top-0 left-[30%]"></div>
        <div className="absolute w-[1px] h-[40%] bg-[#00BFFF] top-[20%] left-[70%]"></div>
        <div className="absolute w-[1px] h-[30%] bg-[#FF1D58] top-[50%] left-[20%]"></div>
        <div className="absolute w-[1px] h-[20%] bg-[#7ED321] top-[60%] left-[80%]"></div>
        
        {/* Nodes/connection points */}
        <div className="absolute w-2 h-2 rounded-full bg-[#7ED321] top-[20%] left-[30%]"></div>
        <div className="absolute w-2 h-2 rounded-full bg-[#00BFFF] top-[40%] right-[10%]"></div>
        <div className="absolute w-2 h-2 rounded-full bg-[#FF1D58] top-[60%] left-[20%]"></div>
        <div className="absolute w-2 h-2 rounded-full bg-[#7ED321] top-[80%] right-[15%]"></div>
      </div>
      
      {/* Subtle glow effects */}
      <div className="absolute top-[10%] left-[10%] w-[300px] h-[300px] rounded-full bg-[#7ED321] opacity-[0.03] blur-[80px]"></div>
      <div className="absolute bottom-[20%] right-[15%] w-[250px] h-[250px] rounded-full bg-[#00BFFF] opacity-[0.03] blur-[70px]"></div>
      <div className="absolute top-[60%] left-[60%] w-[200px] h-[200px] rounded-full bg-[#FF1D58] opacity-[0.03] blur-[60px]"></div>
    </div>
  );
}