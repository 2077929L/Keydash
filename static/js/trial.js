(function($) {
 var word_list = ['coins','emerg','fritt','newel','peasy', 'peepy', 'rewle', 'roopy', 'senex']
 var current_word = word_list[ Math.floor( (Math.random() * 9)) ]
 var current_character = 0;
 var last_update = Date.now();
 var timer = 0;
 var words_complete = 0;
 var flashing = false;
 var game_active = false;
 var key_presses = 0;
 var correct_keys = 0;

 var menu;

  window.app = {

    init: function() {
      var game_frame = $('#game_frame')
      var ui = $('<div/>', { id: 'ui_bar'});
      menu = $('<div />', {id: 'game_overlay'})
      game_frame.append(ui);
      game_frame.append(menu);

      var that= this;

      menu.append($('<div/>', {id: 'game_overlay_title'}).text("KeyDash"))
          .append($('<div/>', {id: 'game_overlay_body'}).html("<h3>Trial Version</h3> <br />This is the trial version of KeyDash, Your results will not be stored and words/modes are limited"))
          .append( $('<div />', {id: 'game_overlay_button'}).hover(function() {
            $(this).animate({backgroundColor: "rgb( 20, 20, 20 )"}, { queue: false, duration: 'slow'});
          }, function() {
            $(this).animate({backgroundColor: "rgb( 20, 20, 20 )"}, { queue: false, duration: 'slow'});
          }).click(function() {
            menu.css('visibility', 'hidden');
            timer = 0;
            words_complete = 0;
            key_presses = 0;
            correct_keys = 0;
            current_word = word_list[ Math.floor( (Math.random() * 9)) ]
            game_active = true;
            current_character = 0
            that.refreshWord()
            $('#ui_wpm').text("0 WPM" )
          }).text("Play"))

      ui.append($('<div/>', {id: 'ui_wpm'}).text('0 wpm'))
      ui.append($('<div/>', {id: 'ui_timer'}).text('60 seconds'))
      ui.append($('<div/>', {class: 'clear_fix'}))
      game_frame.append($('<div/>', {id: 'word_frame'} ))

      $('#word_frame').append( $('<span/>', {class: 'word_done'}) ).append( $('<span/>', {class: 'word_left'}))
      this.refreshWord()
    },

    update: function() {
      window.requestAnimationFrame(function() {
        window.app.update();
      });

      var delta = (Date.now() - last_update) / 1000;
      
      last_update = Date.now();

      if(game_active) {
        timer += delta;
        $('#ui_timer').text((60.0  - timer).toFixed(2) + ' Seconds');

        if(timer > 60.0) {
          game_active = false;
          $('#game_overlay_body').html("<h3>Trial Version</h3> <br />You typed at a rate of " +  words_complete + "WMP with an accuracy of " + ((correct_keys / key_presses) * 100).toFixed(2) + "%")
          $('#game_overlay_button').text("Retry");
          menu.css('visibility', 'visible');
        } else if(timer > 50 && !flashing) {
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

            current_word = word_list[ Math.floor( (Math.random() * 9)) ]
            $('#ui_wpm').text((words_complete / (timer / 60)).toFixed(1) + "WPM" )

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

})(jQuery);