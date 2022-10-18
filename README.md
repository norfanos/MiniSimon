<div align="center" style="padding:0.5em 1.0em 1.0em 1.0em;">
  <h1 style="font-weight:bold;margin:0;adding:0;">CircuitPython KB2040</h1>
  <h2 style="font-weight:bold;margin:0 0 1.0em 0;adding:0;">Mini Simon Game</h2>
  <img src="img/img_0038.png?raw=true" style="width:50%;border:0.2em solid #fff;">
</div>


### The Begining ...

So, I buy a lot of components and wanted to build something out of stuff on hand. Recently I bought a "[step-switch](https://www.adafruit.com/product/5516)" that [Adafruit](https://www.adafruit.com/) started carrying and wanted to build something around it, but wasn't ready for a massive audio based project. I decided creating a mini Simon like game would be a good use of some time and fun to play and share with the kids. Dare I say even inspire them to create.

So I gathered the parts I thought would work well. A piezo speaker, a small I2C SSD1306 based OLED, protoboard, an [Adafruit KB2040](https://www.adafruit.com/product/5302). I later added a small protoboard friendly momentary push button to augment the KB2040's onboard button.

<div align="center" style="padding:0.5em 1.0em 1.0em 1.0em;">
  <img src="img/img_0021.png?raw=true" style="width:50%;border:0.2em solid #fff;">
</div>

My process on this would be organic—in otherwords—I had no real plan. :laughing: So I pulled the parts and began laying out the parts for fitment. It's not the final layout, but if I were to redo it, I would probably aim for this layout only because it would be easier for the OLED screen. You will see in the final images that I went with a portrait layout.

<div align="center" style="padding:0.5em 1.0em 1.0em 1.0em;">
  <img src="img/img_0022.png?raw=true" style="width:50%;border:0.2em solid #fff;">
</div>

That done, I wanted to change the LED on the switches to match the switch's button. So I went all out and took it all apart, not realizing *__I could have just stopped at pulling the colored button off only__*.:unamused: Luckily I didn't damage the switches, and hopefully you can avoid the risk. The LEDs on these switches are 3mm and I had a bunch. So I swapped out all but the red because, hey it's already red. :wink:

<div align="center" style="padding:0.5em 1.0em 1.0em 1.0em;">
  <img src="img/img_0024.png?raw=true" style="width:50%;border:0.2em solid #fff;">
</div>

Once you pop the colored cover/button you can easily pull the LED out and slide the replacement LED in its place. Careful as the holes are small and the wire threshold might be tight. Also pay attention the polarity. The longer one is the positive lead.

<div align="center" style="padding:0.5em 1.0em 1.0em 1.0em;">
  <img src="img/img_0027.png?raw=true" style="width:50%;border:0.2em solid #fff;">
</div>

Once you get them all set, and replace the button back on, I snipped the leads so that once I placed them on the protoboard it would not hold up the project any more than the other pins.

<div align="center" style="padding:0.5em 1.0em 1.0em 1.0em;">
  <img src="img/img_0026.png?raw=true" style="width:50%;border:0.2em solid #fff;">
</div>

I think you'll agree it looks better with the colored LED.

<div align="center" style="padding:0.5em 1.0em 1.0em 1.0em;">
  <img src="img/img_0028.png?raw=true" style="width:50%;border:0.2em solid #fff;">
</div>

Especially for a project that will mimic the classic game of Simon.

<div align="center" style="padding:0.5em 1.0em 1.0em 1.0em;">
  <h2 style="margin:0 0 0.5em 0;adding:0;">Classic Simon Game</h2>
  <a href="https://en.wikipedia.org/wiki/Simon_(game)"><img src="https://upload.wikimedia.org/wikipedia/commons/thumb/c/cd/Simon_Electronic_Game.jpg/220px-Simon_Electronic_Game.jpg" style="width:50%;border:0.2em solid #000;background-color:#fff;padding:1.0em;"><br/>Wiki :arrow_upper_right:</a>
</div>
