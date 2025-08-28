import React, { useState, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
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
    <div className="min-h-screen bg-gradient-to-r from-black via-purple-900 to-slate-900">
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
            
            {!showChat && <Footer />}
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  )
}

export default App