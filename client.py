def aplayer( name ): 
  import pymedia.muxer as muxer, pymedia.audio.acodec as acodec, pymedia.audio.sound as sound 
  import time 
  snd= dec= None 

  dm= muxer.Demuxer( str.split( name, '.' )[ -1 ].lower() ) 
  f= open( name, 'rb' ) 
  s= f.read( 32000 ) 

  while len( s ): 
    frames= dm.parse( s ) 
    if frames: 
      for fr in frames: 
        # Assume for now only audio streams 
        if dec== None: 
          print dm.getInfo(), dm.streams 
          dec= acodec.Decoder( dm.streams[ fr[ 0 ] ] ) 
        
        r= dec.decode( fr[ 1 ] ) 
        if r and r.data: 
          if snd== None: 
            snd= sound.Output( int( r.sample_rate ), r.channels, sound.AFMT_S16_LE, 0 ) 
          
          data= r.data 
          snd.play( data ) 
    
    s= f.read( 512 ) 

  while snd.isPlaying(): 
    time.sleep( .05 )
aplayer("song.mp3")