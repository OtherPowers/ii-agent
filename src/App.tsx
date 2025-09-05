import React, { useState, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { Sparkles } from 'lucide-react'
import Header from './components/Header'
import Hero from './components/Hero'
import Features from './components/Features'
import ChatInterface from './components/ChatInterface'
import Footer from './components/Footer'
import LoadingScreen from './components/LoadingScreen'

function App() {
  const [isLoading, setIsLoading] = useState(true)
  const [showChat, setShowChat] = useState(false)

  useEffect(() => {
    const timer = setTimeout(() => {
      setIsLoading(false)
    }, 2000)

    return () => clearTimeout(timer)
  }, [])

  const handleStartChat = () => {
    setShowChat(true)
  }

  return (
    <div className="min-h-screen bg-white">
      <AnimatePresence mode="wait">
        {isLoading ? (
          <LoadingScreen key="loading" />
        ) : (
          <motion.div
            key="main"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.5 }}
            className="relative"
          >
            <Header />
            
            <AnimatePresence mode="wait">
              {!showChat ? (
                <motion.div
                  key="landing"
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, y: -20 }}
                  transition={{ duration: 0.5 }}
                >
                  <Hero onStartChat={handleStartChat} />
                  <Features />
                </motion.div>
              ) : (
                <motion.div
                  key="chat"
                  initial={{ opacity: 0, scale: 0.95 }}
                  animate={{ opacity: 1, scale: 1 }}
                  transition={{ duration: 0.5 }}
                >
                  <ChatInterface onBack={() => setShowChat(false)} />
                </motion.div>
              )}
            </AnimatePresence>
            
            {!showChat && (
              <motion.div
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.8 }}
                viewport={{ once: true }}
                className="py-16 px-6 text-center"
              >
                <div className="inline-flex items-center space-x-2 bg-gray-100 rounded-full px-4 py-2 webflow-shadow">
                  <Sparkles className="w-4 h-4 text-gray-700" />
                  <span className="text-gray-700 text-sm">Powered by Advanced AI and Humans who believe in less awful futures (together)</span>
                </div>
              </motion.div>
            )}
            
            {!showChat && <Footer />}
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  )
}

export default App