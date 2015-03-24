(function($) {
  var x = 0;
  var target = null;
  var score = 0;
  var lives = 8;

  var dictionary = [];
  var fetching = false;

  var keyspressed = 0;
  var keyscorrect = 0;
  var gamestart = 0;
  var words_complete = 0;

  var extend = function(klass, base) {
    klass.prototype = Object.create(base.prototype);
    klass.prototype.constructor = klass;
  }

  function TextGameObject(scene, spritename, text) {
    SpriteEngine.GameObject.call(this, scene, spritename);
    var newtext = jQuery('<div/>', {
      class: 'hovertext'
    })

    newtext.html(text);
    this.text = text;
    this.text_dom = newtext;
    this.dom_obj.append(newtext);
  }
  extend(TextGameObject, SpriteEngine.GameObject);

  TextGameObject.prototype.overlap = function(object) {
    return (object.position.x > this.position.x);
  }


  function MenuState(scene) {
    GameFramework.State.call(this, scene);
  }
  extend(MenuState, GameFramework.State);

  MenuState.prototype.focus = function() {
    var gui = $("#game_frame");
    var that = this;
    gui.append(jQuery('<div/>', {id: 'game_popup'}).text("Typing Flight").append(jQuery('<div/>', {id: 'scorebox', style: 'font-size: 0.4em;'})).append(jQuery('<div/>', {id: 'game_popup_buuton'}).text("Play").click(function(e) {
      that.framework.popState();
      that.framework.pushState(new GameState(that.scene));
    })));
  }

  MenuState.prototype.blur = function() {
    $("#game_popup").remove();
  }


  function ScoreState(scene, score) {
    GameFramework.State.call(this, scene);
    var accuracy = keyspressed > 0 ? ((keyscorrect / keyspressed) * 100).toFixed(2) : 100;
    var game_length = (Date.now() - gamestart) / 1000;
    var wpm = ((words_complete / game_length) * 60).toFixed(2);
    this.score = score;
    $.post("savescore/", {csrfmiddlewaretoken: $("#csrf_token").val(), game_type: "typingflight", wpm: wpm, accuracy: accuracy, score: score}, function(result){});
  }
  extend(ScoreState, GameFramework.State);

  ScoreState.prototype.focus = function() {
    var gui = $("#game_top_gui");
    var that = this;
    gui.append(jQuery('<div/>', {id: 'game_popup'}).text("Game Over").append(jQuery('<div/>', {id: 'scorebox', style: 'font-size: 0.4em;'}).text("Score: " + this.score)).append(jQuery('<div/>', {id: 'game_popup_buuton'}).text("Retry").click(function(e) {
      that.framework.popState();
      that.framework.resetState();
    })));
  }

  ScoreState.prototype.blur = function() {
    $("#game_popup").remove();
  }



  function GameState(scene) {
    GameFramework.State.call(this, scene);
    //load resources
    this.scene.loadSprite('humvee', 1, 0, true);
    this.scene.loadSprite('helicopter', 1, 0, true);
    this.scene.loadSprite('explosion', 49, 30, false);
    this.scene.loadSprite('explosion_tiny', 49, 30, false);
    this.scene.loadSprite('bullet', 1, 0, true);
    this.scene.loadSprite('plane', 1, 0, true);

    this.scene.loadSound('bullet', '/static/sounds/M1GarandSingle.mp3');
    this.scene.loadSound('boom', '/static/sounds/Explosion2.mp3');

    //build DOM
    jQuery('<div/>', {
      id: 'game_background'
    }).appendTo('#game_frame');

    jQuery('<div/>', {
      id: 'game_ground'
    }).appendTo('#game_frame');

    var gui = jQuery('<div/>', {
      id: 'game_top_gui'
    }).appendTo('#game_frame');

    jQuery('<div/>', {
      id: 'game_score'
    }).appendTo('#game_top_gui');

    jQuery('<div/>', {
      id: 'game_active_word'
    }).appendTo('#game_top_gui').html('<br />');

    jQuery('<div/>', {
      id: 'game_lives'
    }).appendTo('#game_top_gui');

    //add entities
    this.scene.objects.enemy = [];
    new SpriteEngine.GameObject(this.scene, 'helicopter').setGroup('player').setRotation(10).setPosition(100, 100);
  }
  extend(GameState, GameFramework.State);

  GameState.prototype.reset = function() {
    lives = 8;
    score = 0;
    this.scene.clearGroup('enemy');
    this.scene.clearGroup('player_munition');
    target = null;
    keyspressed = 0;
    keyscorrect = 0;
    words_complete = 0;
    gamestart = Date.now();
  }

  GameState.prototype.destroy = function() {
    $("#game_background").remove();
    $("#game_ground").remove();
    $("#game_top_gui").remove();
    this.scene.clear();
  }

  GameState.prototype.update = function(delta) {
    GameFramework.State.prototype.update.call(this, delta);

    if(lives <= 0) {
      this.framework.pushState(new ScoreState(this.scene, score));
      return;
    }

    x-=30 * delta;
    this.scene.objects.enemy.forEach(function(object) {
      if (object.position.x < -100) {
        if (object.incomming === undefined) {
          object.kill();
          if (target === object) {
            target = null;
          }
          lives -= 1;
        } else if (object.incomming.length === 0) {
          object.kill();
          if (target === object) {
            target = null;
          }
          lives -= 1;
        }
      }
      if (object.position.x < 200) {
        object.text_dom.css('background-color', 'grey');
        object.dom_obj.css('z-index', '1000');
        if (object === target) {
          target = null;
        }
      }
      if (object.incoming !== undefined) {
        object.incoming.forEach(function(bullet) {
          if (object.overlap(bullet)) {
            if (object.text.length === object.char_id && object.incoming.length === 1) {
              bullet.scene.playSound('boom', 0.01, 1.0 + Math.random());
              new SpriteEngine.GameObject(bullet.scene, 'explosion').setGroup('effect').setPosition(bullet.position.x, bullet.position.y);
              object.kill();
              score += 100;
              words_complete++;
            } else {
              new SpriteEngine.GameObject(bullet.scene, 'explosion_tiny').setGroup('effect').setPosition(bullet.position.x, bullet.position.y);
              score += 10;
            }
            object.incoming.splice(object.incoming.indexOf(bullet), 1);
            bullet.kill();
          }
        });
      }
    });

    this.scene.objects.player[0].setPosition(this.scene.objects.player[0].position.x, 100 + (20 * Math.sin(x / 50)));

    if (dictionary.length > 1) {
      //spawn
      if (Math.random() > 0.995) {
        new TextGameObject(this.scene, 'humvee', dictionary.shift()).setGroup('enemy').setPosition(850, 365).setVelocity(-60, 0);
      }
      if (Math.random() > 0.997) {
        new TextGameObject(this.scene, 'plane', dictionary.shift()).setGroup('enemy').setPosition(850, 50 + (150 * Math.random())).setVelocity(-90, 0);
      }
    }
    if (dictionary.length < 6 && fetching != true) {
      fetching = true;

      $.getJSON( "newwords/typingflight/", function( data ) {
        dictionary = data.words;
        fetching = false;
      });
    }

    //scroll background
    $("#game_background").css("backgroundPosition", x * 1.5 + 'px' + ' ' + '0px');
    $("#game_ground").css("backgroundPosition", x / 2 + 'px' + ' ' + '0px');

    //update gui
    $("#game_score").html("Score: " + score);
    $("#game_lives").html("Lives: " + lives);

    if (target != null) {
      var done = target.text.substring(0, target.char_id);
      var left = target.text.substring(target.char_id);

      $("#game_active_word").html("<span style = 'color: red;'>" + done + "</span>" + "<span>" + left + "</span>");
    } else {
      $("#game_active_word").html("<br />");
    }

    this.scene.draw();
  }

  GameState.prototype.targetEnemy = function(startingwith) {

    var playerloc = this.scene.objects.player[0].position;
    var closest = Number.MAX_VALUE;
    var closest_enemy = null;
    
    this.scene.objects.enemy.forEach(function(object) {
      var enemyloc = object.position;
      var distance = Math.pow(enemyloc.x - playerloc.x, 2) + Math.pow(enemyloc.y - playerloc.y, 2);
      if (distance < closest && object.text.length !== object.char_id && object.position.x > 200) {
        if (startingwith === undefined) {
          closest = distance;
          closest_enemy = object;
        } else if (startingwith === object.text[0]) {
          closest = distance;
          closest_enemy = object;
        }
      }
    });

    if (closest_enemy != target && closest_enemy !== null) {
      if (target !== null) {
        target.text_dom.css('background-color', 'white');
        target.dom_obj.css('z-index', '1000');
      }
      target = closest_enemy;
      target.text_dom.css('background-color', 'red');
      target.dom_obj.css('z-index', '2000');
      if (target.char_id === undefined) {
        target.char_id = 0;
      }
    }

  }

  GameState.prototype.keyPress = function(e) {
    var chCode = ('charCode' in e) ? e.charCode : e.keyCode;
    var keyPressed = String.fromCharCode(chCode);
    keyspressed ++;
    if (target === null) {
      this.targetEnemy(keyPressed);
      if (target === null) {
        return;
      }
    }

    if (keyPressed === target.text[target.char_id]) {
      target.char_id += 1;
      keyscorrect++;
      if(keyPressed == " ") {
        words_complete++;
      }

      var playerloc = this.scene.objects.player[0].position;
      //gun offset
      var gunoffset = {
        x: 60,
        y: 25
      }

      var deltax = (target.position.x) - (playerloc.x + gunoffset.x);
      var deltay = (target.position.y) - (playerloc.y + gunoffset.y);
      var deltamag = Math.sqrt(Math.pow(deltax, 2) + Math.pow(deltay, 2));

      //TODO: probably to wastfull to be usefull
      var leaddistance = (deltamag / 500) * target.velocity.x;
      deltax = (target.position.x + leaddistance) - (playerloc.x + gunoffset.x);
      deltay = (target.position.y) - (playerloc.y + gunoffset.y);
      deltamag = Math.sqrt(Math.pow(deltax, 2) + Math.pow(deltay, 2));
      //**************

      deltax /= deltamag;
      deltay /= deltamag;

      if (target.incoming === undefined) {
        target.incoming = [];
      }

      this.scene.playSound('bullet', 0.01);
      target.incoming.push(new SpriteEngine.GameObject(this.scene, 'bullet').setGroup('player_munition').setPosition(playerloc.x + gunoffset.x, playerloc.y + gunoffset.y).setVelocity(deltax * 500, deltay * 500));

      if (target.char_id == target.text.length) {
        target.text_dom.css('background-color', 'green');
        target.dom_obj.css('z-index', '1000');
        target = null;
      }
    }
  }

  GameState.prototype.keyDown = function(e) {
    var keyCode = e.keyCode || e.which;
    if (keyCode == 9) { //tab
      e.preventDefault();
      this.targetEnemy();
    }
    if (keyCode == 8) {//backspace
      e.preventDefault();
    }
  }

  window.app = {
    init: function() {
      this.scene = new SpriteEngine.Scene("#game_frame");
      this.framework = new GameFramework.Framework("body");
      //this.framework.pushState(new GameState(this.scene));
      this.framework.pushState(new MenuState(this.scene));
      this.framework.start();
    },
  }

  $(document).ready(function() {
    window.app.init();
  });


})(jQuery);