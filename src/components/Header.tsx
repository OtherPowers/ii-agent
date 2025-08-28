import React from 'react'
import { motion } from 'framer-motion'
import { Github, MessageSquare, Settings } from 'lucide-react'

const Header = () => {
  return (
    <motion.header
      initial={{ y: -100, opacity: 0 }}
      animate={{ y: 0, opacity: 1 }}
      transition={{ duration: 0.8, ease: "easeOut" }}
      className="fixed top-0 left-0 right-0 z-40 glass-effect"
    >
      <div className="container mx-auto px-6 py-4">
        <div className="flex items-center justify-between">
          <motion.div
            whileHover={{ scale: 1.05 }}
            className="flex items-center space-x-3"
          >
            <div className="w-10 h-10 bg-gradient-to-br from-blue-400 to-purple-600 rounded-xl flex items-center justify-center">
              <span className="text-white font-bold text-lg">II</span>
            </div>
            <div>
              <h1 className="text-xl font-bold text-white">II-Agent</h1>
              <p className="text-xs text-white/60">Intelligent Assistant Platform</p>
            </div>
          </motion.div>
          
          <nav className="hidden md:flex items-center space-x-6">
            <motion.a
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              href="#features"
              className="text-white/80 hover:text-white transition-colors"
            >
              Features
            </motion.a>
            <motion.a
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              href="#capabilities"
              className="text-white/80 hover:text-white transition-colors"
            >
              Capabilities
            </motion.a>
            <motion.a
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              href="https://github.com/Intelligent-Internet/ii-agent"
              target="_blank"
              rel="noopener noreferrer"
              className="text-white/80 hover:text-white transition-colors"
            >
              <Github className="w-5 h-5" />
            </motion.a>
          </nav>
          
          <div className="flex items-center space-x-3">
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              className="p-2 glass-effect rounded-lg text-white/80 hover:text-white transition-colors"
            >
              <Settings className="w-5 h-5" />
            </motion.button>
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              className="p-2 glass-effect rounded-lg text-white/80 hover:text-white transition-colors"
            >
              <MessageSquare className="w-5 h-5" />
            </motion.button>
          </div>
        </div>
      </div>
    </motion.header>
  )
}

export default Header