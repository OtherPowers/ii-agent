import React from 'react'
import { motion } from 'framer-motion'

const LoadingScreen = () => {
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
          <div className="w-32 h-32 mx-auto mb-6 relative overflow-hidden rounded-full">
            {/* Oil-in-water holographic lava lamp container */}
            <div className="lava-lamp-container">
              <div className="lava-lamp-blobs">
                <svg viewBox="0 0 1200 1200" className="w-full h-full">
                  {/* Main blobs */}
                  <g className="blob blob-1">
                    <motion.path
                      animate={{
                        d: [
                          "M 100 600 q 0 -500, 500 -500 t 500 500 t -500 500 T 100 600 z",
                          "M 100 600 q -50 -400, 500 -500 t 450 550 t -500 500 T 100 600 z",
                          "M 100 600 q 0 -400, 500 -500 t 400 500 t -500 500 T 100 600 z",
                          "M 150 600 q 0 -600, 500 -500 t 500 550 t -500 500 T 150 600 z"
                        ]
                      }}
                      transition={{
                        duration: 5,
                        repeat: Infinity,
                        ease: "easeInOut"
                      }}
                      fill="#984ddf"
                      style={{ filter: 'blur(1rem)', opacity: 0.7 }}
                    />
                  </g>
                  <g className="blob blob-2">
                    <motion.path
                      animate={{
                        d: [
                          "M 100 600 q 0 -400, 500 -500 t 400 500 t -500 500 T 100 600 z",
                          "M 150 600 q 0 -600, 500 -500 t 500 550 t -500 500 T 150 600 z",
                          "M 100 600 q 100 -600, 500 -500 t 400 500 t -500 500 T 100 600 z",
                          "M 100 600 q -50 -400, 500 -500 t 450 550 t -500 500 T 100 600 z"
                        ]
                      }}
                      transition={{
                        duration: 7,
                        repeat: Infinity,
                        ease: "easeInOut",
                        delay: 1
                      }}
                      fill="#4344ad"
                      style={{ filter: 'blur(0.75rem)', opacity: 0.7, transform: 'scale(0.78)' }}
                    />
                  </g>
                  <g className="blob blob-3">
                    <motion.path
                      animate={{
                        d: [
                          "M 100 600 q -50 -400, 500 -500 t 450 550 t -500 500 T 100 600 z",
                          "M 150 600 q 0 -600, 500 -500 t 500 550 t -500 500 T 150 600 z",
                          "M 100 600 q 0 -400, 500 -500 t 400 500 t -500 500 T 100 600 z",
                          "M 100 600 q 100 -600, 500 -500 t 400 500 t -500 500 T 100 600 z"
                        ]
                      }}
                      transition={{
                        duration: 6,
                        repeat: Infinity,
                        ease: "easeInOut",
                        delay: 2
                      }}
                      fill="#74d9e1"
                      style={{ filter: 'blur(0.5rem)', opacity: 0.7, transform: 'scale(0.76)' }}
                    />
                  </g>
                  <g className="blob blob-4">
                    <motion.path
                      animate={{
                        d: [
                          "M 150 600 q 0 -600, 500 -500 t 500 550 t -500 500 T 150 600 z",
                          "M 100 600 q 100 -600, 500 -500 t 400 500 t -500 500 T 100 600 z",
                          "M 100 600 q -50 -400, 500 -500 t 450 550 t -500 500 T 100 600 z",
                          "M 100 600 q 0 -500, 500 -500 t 500 500 t -500 500 T 100 600 z"
                        ]
                      }}
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
            className="text-white/70 text-lg"
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