// Get text description of image using Astica API
// TODO this is still not working - CORS issues
function startAstica() {
    setTimeout(function() {
      asticaAPI_start('AA3BF25A-9358-4FED-B8A3-C767949FDDBAFC07B7E1-8652-4ACF-AACC-A8AB3337F90A')
      asticaVision(
        '1.0_full',
        'https://upload.wikimedia.org/wikipedia/commons/e/e7/Everest_North_Face_toward_Base_Camp_Tibet_Luca_Galuzzi_2006.jpg',
        'Description',
        asticaCallback
      );
    }, 2000);
}

// Add Google Cloud Text to Speech dictation for all speaker icons
/*
  TODO bug: If the prompt_reply spaker is pressed first, then the user clicks the initial_prompt speaker,
  the prompt_reply text will still be read. Clicking initial_prompt a second time will dictate the correct text.
*/
$(document).ready(function() {
    $('.dictate').click(function() {
      var text = $(this).closest('div').prev().find('.text-to-dictate').first().data('prompt');
      $.ajax({
        url: '/dictate',
        type: 'POST',
        data: {text: text},
        success: function(response) {
          console.log(response);
          var audio = new Audio(response.audio_url);
          audio.play();
        },
        error: function(error) {
          console.log(error);
        }
      });
    });
  });