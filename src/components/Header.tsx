import React from 'react'
import { motion } from 'framer-motion'
import { Github, MessageSquare, Settings } from 'lucide-react'

const Header = () => {
  return (
    <motion.header
      initial={{ y: -100, opacity: 0 }}
      animate={{ y: 0, opacity: 1 }}
      transition={{ duration: 0.8, ease: "easeOut" }}
      className="fixed top-0 left-0 right-0 z-40 bg-white/95 backdrop-blur-sm border-b border-gray-200 shadow-lg"
    >
      <div className="container mx-auto px-6 py-4">
        <div className="flex items-center justify-between">
          <motion.div
            whileHover={{ scale: 1.05 }}
            className="flex items-center space-x-3"
          >
            <div className="w-10 h-10 bg-white rounded-xl flex items-center justify-center border border-gray-200">
              <span className="text-gray-500 font-bold text-lg">II</span>
            </div>
            <h1 className="text-xl font-bold text-gray-900">II-Agent</h1>
          </motion.div>
          
          <nav className="hidden md:flex items-center space-x-6">
            <motion.a
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              href="#features"
              className="text-gray-600 hover:text-gray-900 transition-colors"
            >
              Features
            </motion.a>
            <motion.a
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              href="#capabilities"
              className="text-gray-600 hover:text-gray-900 transition-colors"
            >
              Capabilities
            </motion.a>
            <motion.a
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              href="https://github.com/Intelligent-Internet/ii-agent"
              target="_blank"
              rel="noopener noreferrer"
              className="text-gray-600 hover:text-gray-900 transition-colors"
            >
              <Github className="w-5 h-5" />
            </motion.a>
          </nav>
          
          <div className="flex items-center space-x-3">
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              className="p-2 bg-gray-100 rounded-lg text-gray-600 hover:text-gray-900 transition-colors webflow-shadow"
            >
              <Settings className="w-5 h-5" />
            </motion.button>
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              className="p-2 bg-gray-100 rounded-lg text-gray-600 hover:text-gray-900 transition-colors webflow-shadow"
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