import { useEffect, useRef, useState } from "react";
import { motion } from "framer-motion";

// Define terminal commands and responses
const terminalSequence = [
  { 
    command: "grimOS > initializing system...", 
    delay: 800 
  },
  { 
    command: "grimOS > running diagnostics...",
    delay: 1200 
  },
  { 
    command: "grimOS > cognitive core online",
    delay: 1000 
  },
  { 
    command: "grimOS > analyzing telemetry from Cauldron™...",
    delay: 1500 
  },
  { 
    command: "grimOS > neural fabric connected",
    delay: 1000 
  },
  { 
    command: "grimOS > system status: optimal",
    delay: 800 
  },
  { 
    command: "grimOS > phantomIntel™ module activated",
    delay: 1200 
  },
  { 
    command: "grimOS > quantum analysis complete",
    delay: 1000 
  },
  { 
    command: "grimOS > generating business insights...",
    delay: 1500 
  },
  { 
    command: "grimOS > forecast models ready",
    delay: 1000 
  },
  { 
    command: "grimOS > profit optimization strategies loaded",
    delay: 1200 
  },
  { 
    command: "grimOS > ready for instructions",
    delay: 0 
  }
];

export default function CommandTerminal() {
  const [visibleLines, setVisibleLines] = useState<string[]>([]);
  const [currentLine, setCurrentLine] = useState(0);
  const [typing, setTyping] = useState(false);
  const [typingText, setTypingText] = useState("");
  const [cursorVisible, setCursorVisible] = useState(true);
  const terminalRef = useRef<HTMLDivElement>(null);

  // Cursor blink effect
  useEffect(() => {
    const cursorInterval = setInterval(() => {
      setCursorVisible(prev => !prev);
    }, 530);
    
    return () => clearInterval(cursorInterval);
  }, []);

  // Terminal typing effect
  useEffect(() => {
    if (currentLine >= terminalSequence.length) return;
    
    const typeText = async () => {
      const line = terminalSequence[currentLine];
      setTyping(true);
      
      // Type the current line character by character
      for (let i = 0; i < line.command.length; i++) {
        setTypingText(line.command.substring(0, i + 1));
        await new Promise(resolve => setTimeout(resolve, 30 + Math.random() * 40));
      }
      
      setVisibleLines(prev => [...prev, line.command]);
      setTyping(false);
      setTypingText("");
      
      // Schedule the next line
      setTimeout(() => {
        setCurrentLine(prev => prev + 1);
      }, line.delay);
    };
    
    if (!typing) {
      typeText();
    }
  }, [currentLine, typing]);

  // Auto-scroll to the bottom of the terminal
  useEffect(() => {
    if (terminalRef.current) {
      terminalRef.current.scrollTop = terminalRef.current.scrollHeight;
    }
  }, [visibleLines, typingText]);

  return (
    <motion.div 
      className="w-full rounded-xl glass-darker border border-[#7ED321]/20 overflow-hidden"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5, delay: 0.2 }}
    >
      {/* Terminal header */}
      <div className="flex items-center justify-between px-4 py-2 border-b border-[#FFFFFF]/10 bg-[#121212]">
        <div className="flex items-center space-x-1.5">
          <div className="w-3 h-3 rounded-full bg-[#FF5F57]"></div>
          <div className="w-3 h-3 rounded-full bg-[#FFBD2E]"></div>
          <div className="w-3 h-3 rounded-full bg-[#28CA41]"></div>
        </div>
        <div className="text-xs text-[#FFFFFF]/60">grimOS® Terminal</div>
        <div className="text-xs text-[#FFFFFF]/60">v3.7.2</div>
      </div>
      
      {/* Terminal content */}
      <div 
        ref={terminalRef}
        className="p-4 font-mono text-sm h-60 overflow-y-auto scrollbar-thin scrollbar-thumb-[#7ED321]/20 scrollbar-track-transparent"
      >
        {visibleLines.map((line, index) => (
          <div key={index} className="mb-1.5">
            <span className="text-[#7ED321]">{line}</span>
          </div>
        ))}
        
        {typing && (
          <div className="mb-1.5">
            <span className="text-[#7ED321]">
              {typingText}
              <span className={`inline-block w-2 h-4 ml-0.5 bg-[#7ED321] ${cursorVisible ? 'opacity-100' : 'opacity-0'}`}></span>
            </span>
          </div>
        )}
        
        {!typing && currentLine >= terminalSequence.length && (
          <div className="flex items-center">
            <span className="text-[#7ED321]">grimOS</span>
            <span className="text-[#7ED321] ml-1">{`>`}</span>
            <span className={`inline-block w-2 h-4 ml-2 bg-[#7ED321] ${cursorVisible ? 'opacity-100' : 'opacity-0'}`}></span>
          </div>
        )}
      </div>
    </motion.div>
  );
}