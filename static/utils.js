// Add Google Cloud Text to Speech dictation for all speaker icons
/*
  TODO bug: If the prompt_reply speaker is pressed first, then the user clicks the initial_prompt speaker,
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

// BEGIN: Show/hide user input divs
function toggleDiv(divElement, buttonElement) {

  // Check if div is currently visible
  const isVisible = divElement.style.display === 'block';

  // Hide all divs before displaying the clicked one
  const textDiv = document.getElementById('text-div');
  const audioDiv = document.getElementById('audio-div');
  const imageDiv = document.getElementById('image-div');
  textDiv.style.display = 'none';
  audioDiv.style.display = 'none';
  imageDiv.style.display = 'none';

  // Reset button appearance for all buttons
  const textButton = document.getElementById('text-button');
  const audioButton = document.getElementById('audio-button');
  const imageButton = document.getElementById('image-button');
  textButton.classList.remove('is-info');
  textButton.classList.add('is-info', 'is-outlined');
  audioButton.classList.remove('is-info');
  audioButton.classList.add('is-info', 'is-outlined');
  imageButton.classList.remove('is-info');
  imageButton.classList.add('is-info', 'is-outlined');

  // Toggle the display property of the clicked div
  divElement.style.display = isVisible ? 'none' : 'block';

  // Fill the clicked button when its div is displayed
  if (!isVisible) {
    buttonElement.classList.remove('is-outlined');
  }
}

$(document).ready(function() {
  // Get references to the butotns and their respective divs
  const textButton = document.getElementById('text-button');
  const audioButton = document.getElementById('audio-button');
  const imageButton = document.getElementById('image-button');
  const textDiv = document.getElementById('text-div');
  const audioDiv = document.getElementById('audio-div');
  const imageDiv = document.getElementById('image-div');

  // Add event click listeners to the buttons
  textButton.addEventListener('click', () => toggleDiv(textDiv, textButton));
  audioButton.addEventListener('click', () => toggleDiv(audioDiv, audioButton));
  imageButton.addEventListener('click', () => toggleDiv(imageDiv, imageButton));
});

// END: Show/hide user input divs