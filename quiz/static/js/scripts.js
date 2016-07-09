var wpm = 300;

function construct_subcategory_select(category) {
    if (category == "Literature" || category == "History") {
        return ["American", "British", "European", "World", "Classical", "Other"];
    } else if (category == "Science") {
        return ["Biology", "Chemistry", "Physics", "Math", "Computer Science", "Other"];
    } else if (category == "Fine Arts") {
        return ["Auditory", "Visual", "Audiovisual", "Other"];
    }
    return [];
}

function getCookie(name) {
  var value = "; " + document.cookie;
  var parts = value.split("; " + name + "=");
  if (parts.length == 2) return parts.pop().split(";").shift();
}

function Trivia() {
    var current = null;
    this.category = "All";
    this.subcategory = "All";
    this.complete = false;
    var state = {
        animate: 2
    };
    this.state = function() {
        return state;
    }

    this.iterate_animation_state = function() {
        console.log(state.animate);
        if (state.animate > -1 && state.animate < 4) {
            switch(state.animate) {
            case 0:
                document.getElementById('question').textContent += " (#) ";
                break;
            case 1:
                document.getElementById('response').className = "visible";
                document.getElementById('question').textContent += animation_text.join(" ");
                document.getElementById('answer').textContent = current.result.questions[0].answer;
                animation_text = [];
                break;
            case 2:
                state.animate = -1;
                document.getElementById('question').textContent = "";
                document.getElementById('answer').textContent = "";
                document.getElementById('metadata').textContent = "";
                document.getElementById('next_clue').disabled = true;
                document.getElementById('response').className = "invisible";
                break;
            }
            state.animate++;
        }
    }
    
    var animation_text = [];

    /**
     * Loads a random clue from the API.
     */
    this.random = function() {
        this.iterate_animation_state();
        this.random_request(function(e) {
            if (e.error == null) {
                t.load_clue(e.result);
            }
        });
    }

    this.result_post = function(result) {
        var request = new XMLHttpRequest();
        var url = '/api/quiz/result';
        var params = "name=" + current.result.name;
        params += "&result=" + result;
        request.open('POST', url, true); 
        request.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));
        request.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
        request.onreadystatechange = function() {
            if(this.readyState === 4) {
                console.log(this.response);
            }
        }
        request.send(params);
    }

    this.correct = function() {
        console.log("CORRECT!");
        this.result_post("correct");
        this.random();
    }

    this.missed = function() {
        console.log("MISSED!");
        this.result_post("missed");
        this.random();
    }
    
    this.random_request = function(callback) {
        var request = new XMLHttpRequest();
        var url = '/api/quiz/random';
        url += "?category=" + this.category;
        url += "&subcategory=" + this.subcategory;
        request.open('GET', url, true);
        request.onreadystatechange = function() {
            if(this.readyState === 4) {
                current = JSON.parse(this.response);
                callback(current);
            }
        }
        request.send(null);
    }

    /**
     * Populate the document with a clue.
     */
    this.load_clue = function(clue) {
        var a = ["Category: " + clue.category];
        if (clue.subcategory != "") {
            a.push("Subcategory: " + clue.subcategory);
        }
        a.push("ID: " + clue.name);
        document.getElementById('metadata').textContent = a.join(" | ");
        //document.getElementById('question').textContent = clue.questions[0].text;
        document.getElementById('question').textContent = "";
        animate(clue.questions[0]);
        //document.getElementById('answer').textContent = clue.questions[0].answer;
    }

    function animate(question) {
        var offset = 60000 / wpm;
        var current_delay = 0;
        animation_text = question.text.split(" ");
        var len = animation_text.length;
        window.setTimeout(function() {
            if (t.state().animate == 0 && animation_text.length == 0) {
                t.iterate_animation_state();
            }
        }, offset * (len + 1));
        for (word in animation_text) {
            window.setTimeout(function() {
                if (state.animate == 0 && animation_text.length > 0) {
                    document.getElementById('question').textContent += " " + animation_text.shift();
                }
            }, offset * word);
        }
    }
}

var parser = document.createElement('a');
parser.href = document.URL;
if (parser.pathname == "/quizzer") {
    console.info("Quizzer.");
    var t = new Trivia();
    //t.random();
    document.getElementById('next_clue').addEventListener('click', function(e) {
        t.random();
    });
    document.getElementById('subcategory').addEventListener('change', function(e) {
        t.subcategory = e.target.value;
    });
    document.getElementById('category').addEventListener('change', function(e) {
        t.category = e.target.value;
        t.subcategory = "All";
        var options = ["<option>All</option>"];
        construct_subcategory_select(e.target.value).forEach(function(a) {
            options.push("<option>"+a+"</option>");
        });
        document.getElementById('subcategory').innerHTML = options.join();
    });
    document.getElementById('correct').addEventListener('click', t.correct);
    document.getElementById('missed').addEventListener('click', t.missed);
    document.addEventListener('keypress', function(e) {
        switch (e.key) {
            /*
        case "n":
            switch(t.state().animate) {
            case 2:
                t.random();
                break;
            }
            //t.random();
            break;*/
        case "k":
            if (t.state().animate == 2) {
                t.correct();
            }
            break;
        case "j":
            if (t.state().animate == 2) {
                t.missed();
            }
            break;
        case " ":
            if (t.state().animate == 0 || t.state().animate == 1) {
                t.iterate_animation_state();
            }
            break;
        }
    });
}
