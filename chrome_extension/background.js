function resetDefaultSuggestion() {
    chrome.omnibox.setDefaultSuggestion({
      description: "Hit enter to see Google results! Alternatively, try these more fair results..."
    });
  }
  
  resetDefaultSuggestion();
  
  let timeout = null;
  chrome.omnibox.onInputChanged.addListener(function(text, suggest) {
    chrome.omnibox.setDefaultSuggestion({
        description: "Loading fair results..."
      });
    clearTimeout(timeout);
    timeout = setTimeout(function () {
        // const url = "https://cors-anywhere.herokuapp.com/http://www.jayrothenberger.com/test/"
        // const p = {
        //     method: "GET",
        //     query: text
        // };
        x = new XMLHttpRequest();
        x.open('GET', 'https://cors-anywhere.herokuapp.com/http://www.jayrothenberger.com/test/');
        x.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
        x.onload = function() {
            resetDefaultSuggestion();
        };
        x.send();
        // fetch(url, p)
        // .then(data=>{return data.json()})
        // .then(res=>{
        //     resetDefaultSuggestion();
        //     suggest([
        //         {content: "res", description: res},
        //         {content: "https://www.nbcnews.com/politics/donald-trump/trump-takes-victory-lap-after-cheney-s-ouster-house-republican-n1267081", description: "https://www.nbcnews.com/politics/donald-trump/trump-takes-victory-lap-after-cheney-s-ouster-house-republican-n1267081"}
        //     ])
        // })
    }, 1000);
    
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
    if (text.substr(0, 4) == "http") {
        navigate(text)
    }
    else {
        navigate("https://www.google.com/search?q=" + text);
    }
    
  });