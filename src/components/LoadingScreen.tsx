import React, { useEffect } from 'react'
import { motion } from 'framer-motion'

const LoadingScreen = () => {
  useEffect(() => {
    // Initialize the lava lamp effect
    const container = document.querySelector(".loader-container .container");
    const blobs = document.querySelector(".loader-container .blobs");
    
    if (container && blobs) {
      // Set initial palette
      container.classList.add("palette-1");
    }
  }, []);

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      className="fixed inset-0 bg-white flex items-center justify-center z-50"
    >
      <div className="text-center">
        <motion.div
          initial={{ scale: 0.8, opacity: 0 }}
          animate={{ scale: 1, opacity: 1 }}
          transition={{ duration: 0.8, ease: "easeOut" }}
          className="mb-8"
        >
          <div className="loader-container mx-auto mb-6">
            <div className="container palette-1">
              <div className="blobs">
                <svg viewBox="0 0 1200 1200">
                  <g className="blob blob-1">
                    <path />
                  </g>
                  <g className="blob blob-2">
                    <path />
                  </g>
                  <g className="blob blob-3">
                    <path />
                  </g>
                  <g className="blob blob-4">
                    <path />
                  </g>
                  <g className="blob blob-1 alt">
                    <path />
                  </g>
                  <g className="blob blob-2 alt">
                    <path />
                  </g>
                  <g className="blob blob-3 alt">
                    <path />
                  </g>
                  <g className="blob blob-4 alt">
                    <path />
                  </g>
                </svg>
              </div>
            </div>
          </div>
          
          <motion.h1
            initial={{ y: 20, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            transition={{ delay: 0.3, duration: 0.6 }}
            className="text-4xl font-bold gradient-text mb-4"
          >
            II-Agent
          </motion.h1>
          
          <motion.p
            initial={{ y: 20, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            transition={{ delay: 0.5, duration: 0.6 }}
            className="text-gray-600 text-lg"
          >
            Initializing Intelligent Assistant...
          </motion.p>
        </motion.div>
        
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 1, duration: 0.5 }}
          className="flex justify-center space-x-2"
        >
          {[0, 1, 2].map((i) => (
            <motion.div
              key={i}
              animate={{
                scale: [1, 1.2, 1],
                opacity: [0.5, 1, 0.5],
              }}
              transition={{
                duration: 1.5,
                repeat: Infinity,
                delay: i * 0.2,
              }}
              className="w-3 h-3 bg-gray-900 rounded-full"
            />
          ))}
        </motion.div>
      </div>
    </motion.div>
  )
}

export default LoadingScreen