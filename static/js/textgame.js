function getQueryVariable(variable) {
       var query = window.location.search.substring(1);
       var vars = query.split("&");
       for (var i=0;i<vars.length;i++) {
               var pair = vars[i].split("=");
               if(pair[0] == variable){return pair[1];}
       }
       return(false);
}

(function($) {
  var game_length = 5
  var word_list = []
  var current_word = ""
  var current_character = 0
  var last_update = Date.now();
  var timer = 0;
  var words_complete = 0;
  var flashing = false;
  var game_active = false;
  var key_presses = 0;
  var correct_keys = 0;
  var menu;
  var game_type = getQueryVariable('game_mode');

  window.app = {

    init: function() {
      this.getNewData();
      var game_frame = $('#game_frame')
      var ui = $('<div/>', { id: 'ui_bar'});
      menu = $('<div />', {id: 'game_overlay'})
      game_frame.append(ui);
      game_frame.append(menu);

      var that = this;

      menu.append($('<div/>', {id: 'game_overlay_title'}).text("KeyDash"))
          .append($('<div/>', {id: 'game_overlay_body'}).html(game_type))
          .append( $('<div />', {id: 'game_overlay_button'}).hover(function() {
            $(this).animate({backgroundColor: "rgb( 20, 20, 20 )"}, { queue: false, duration: 'slow'});
          }, function() {
            $(this).animate({backgroundColor: "rgb( 20, 20, 20 )"}, { queue: false, duration: 'slow'});
          }).click(function() {
            if(word_list.length > 0) {
              menu.css('visibility', 'hidden');
              timer = 0;
              words_complete = 0;
              key_presses = 0;
              current_word =  that.randomWordFromList(word_list);
              game_active = true;
              current_character = 0
              that.refreshWord()
            }

            $('#ui_wpm').text("0 WPM" )
          }).text("Play"))

      ui.append($('<div/>', {id: 'ui_wpm'}).text('0 wpm'))
      ui.append($('<div/>', {id: 'ui_timer'}).text(game_length +' seconds'))
      ui.append($('<div/>', {class: 'clear_fix'}))
      game_frame.append($('<div/>', {id: 'word_frame'} ))

      $('#word_frame').append( $('<span/>', {class: 'word_done'}) ).append( $('<span/>', {class: 'word_left'}))
    },

    update: function() {
      window.requestAnimationFrame(function() {
        window.app.update();
      });

      var delta = (Date.now() - last_update) / 1000;
      
      last_update = Date.now();

      if(game_active) {
        timer += delta;
        $('#ui_timer').text((game_length - timer).toFixed(2) + ' Seconds');

        if(timer >game_length) {

          var accuracy = key_presses > 0 ? ((correct_keys / key_presses) * 100).toFixed(2) : 100
          var wpm = ((words_complete / game_length) * 60).toFixed(2)

          this.sendScore(wpm, accuracy)


          game_active = false;
          $('#game_overlay_body').html("<h3>Game Over</h3> <br />You typed at a rate of " +  wpm  + "WMP with an accuracy of " + accuracy + "%")
          $('#game_overlay_button').text("Retry");
          menu.css('visibility', 'visible');
        } else if(timer > (game_length - 10) && !flashing) {
          flashing = true;
          $('#ui_timer').css('color: rgb(255,0,0)');
          $('#ui_timer').fadeOut('fast').fadeIn('fast', function() {
            flashing = false;
          });
        }
      }
    },

    refreshWord: function() {
        var done = current_word.substring(0, current_character);
        var left = current_word.substring(current_character);
        $(".word_left").text(left)
        $(".word_done").text(done)
    },

    getNewData: function() {
      $.getJSON( "newwords/" + game_type, function( data ) {
        word_list = data.words
      });
    },

    randomWordFromList: function(list) {
      if (list.length == 0) return undefined;

      var index = Math.floor(Math.random()*list.length);
      var newword = list[index];
      //remove element from list
      if (index > -1) {
          list.splice(index, 1);
      }
      return newword;
    },

    sendScore: function(wpm, accuracy) {
      $.getJSON( "savescore/" + game_type + "/" + wpm + "/" + accuracy + "/", function( data ) {
        console.log(data)
      });
    },

    keypress: function(e) {
        if(game_active) {
          key_presses ++;
          var chCode = ('charCode' in e) ? e.charCode : e.keyCode;
          var keyPressed = String.fromCharCode(chCode);

          if (keyPressed === current_word[current_character]) {
            current_character += 1;
            correct_keys ++ ;
          }

          if(current_word.length == current_character) {
            current_character = 0;
            words_complete ++;
            var finished_word = $('<div/>', {class: 'complete_word'}).text(current_word);
            $('#word_frame').append(finished_word);
            finished_word.animate({ 'opacity' : '0', 'top': '50' }, { queue: false, duration: 'slow', complete: function() {
              finished_word.remove();
            }});

            current_word = this.randomWordFromList(word_list);
            if(word_list.length < 5) {
              this.getNewData();
            }
            $('#ui_wpm').text((words_complete / (timer / game_length)).toFixed(1) + "WPM" );

          }

          this.refreshWord()
        }
    },

    keydown: function(e) {
      var keyCode = e.keyCode || e.which;
      if (keyCode == 8) { //tab
        e.preventDefault();
      }
    }
  }

  $(document).ready(function() {
    window.app.init();
    window.app.update();
  });

  $("body").keypress(function(e) {
    window.app.keypress(e);
  });

  $("body").keydown(function(e) {
    window.app.keydown(e);
  });

  $('input[type=radio]').click(function() {
    $(this).closest("form").submit();
  });

})(jQuery);