// Engine-level contracts shared by every mode implementation.

                                           

                                                  

                                       

/**
 * Geometry for one instant: pure math over (size, t, opts), no rendering
 * surface and no theme — `dark` only affects ink at paint time.
 *
 * Deliberately closure-free and `Math`-only so the same function can run
 * inside a Reanimated worklet on the React Native UI thread, and so its
 * output can be compared numerically against the Swift port.
 */
                                                                              

/** One frame painter: draws a mode into a 2D context at CSS-px `size`. */
                        
                                
               
            
                
                
          
