function resetDefaultSuggestion() {
    chrome.omnibox.setDefaultSuggestion({
      description: 'Hit enter when done with your query!'
    });
  }
  
  resetDefaultSuggestion();
  
  chrome.omnibox.onInputChanged.addListener(function(text, suggest) {
    // Suggestion code will end up here.
  });
  
  chrome.omnibox.onInputCancelled.addListener(function() {
    resetDefaultSuggestion();
  });
  
  function navigate(url) {
    chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
      chrome.tabs.update(tabs[0].id, {url: url});
    });
  }
  
  chrome.omnibox.onInputEntered.addListener(function(text) {
    // get de-biased text
    debiased = text;
    navigate("https://www.google.com/search?q=" + "A DEBIASED VERSION OF " + debiased);
  });