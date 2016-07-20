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
        animate: 2,
        buzz_points: 0
    };
    this.state = function() {
        return state;
    }

    this.iterate_animation_state = function() {
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
        params += "&buzz_points=" + state.buzz_points;
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
        this.result_post(true);
        this.random();
    }

    this.missed = function() {
        this.result_post(false);
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
        document.getElementById('question').textContent = "";
        animate(clue.questions[0]);
    }

    function animate(question) {
        var offset = 60000 / wpm;
        animation_text = [];
        animation_text = question.text.split(" ");
        var len = animation_text.length;
        state.buzz_points = len;
        window.setTimeout(function() {
            if (t.state().animate == 0 && animation_text.length == 0) {
                t.iterate_animation_state();
            }
        }, offset * len + 3000);
        for (word in animation_text) {
            window.setTimeout(function() {
                if (state.animate == 0 && animation_text.length > 0) {
                    document.getElementById('question').textContent += " " + animation_text.shift();
                    state.buzz_points--;
                }
            }, offset * word);
        }
    }
}

function Search(term) {
    this.term = term;
    var results;
    this.query = function(callback) {
        var request = new XMLHttpRequest();
        var url = '/api/quiz/search';
        url += "?term=" + this.term;
        request.open('GET', url, true);
        request.onreadystatechange = function() {
            if(this.readyState === 4) {
                results = JSON.parse(this.response);
                callback(results);
            }
        }
        request.send(null);
    }

    this.to_html = function() {
        var r = document.getElementById("results");
        while (r.firstChild) {
            r.removeChild(r.firstChild);
        }
        if (results && results.error == null && results.result.items.length > 0) {
            results.result.items.forEach(function(c) {
                var div = document.createElement("div");
                var meta = document.createElement("p");
                meta.innerText = "ID: " + c.name + " | " + c.category + " | " + c.subcategory;
                div.appendChild(meta);
                var w = document.createElement("div");
                c.questions.forEach(function(z) {
                    var q = document.createElement("p");
                    q.innerText = "Question: " + z.text;
                    w.appendChild(q);
                    var a = document.createElement("p");
                    a.innerText = "Answer: " + z.answer;
                    w.appendChild(a);
                });
                r.appendChild(div);
                r.appendChild(w);
            });
        } else {
            var no = document.createElement("p");
            no.innerText = "No Results found";
            r.appendChild(no);
        }
    }

    this.named_entities = function() {
        var r = document.getElementById("named_entities");
        while (r.firstChild) {
            r.removeChild(r.firstChild);
        }
        if (results && results.error == null && results.result.entities.length > 0) {
            var list = document.createElement("ol");
            results.result.entities.forEach(function(e) {
                var item = document.createElement("li");
                item.innerText = e.term + " (" + e.num + ")";
                list.appendChild(item);
            });
            r.appendChild(list);
        } else {
            var no = document.createElement("p");
            no.innerText = "No named entities recognized.";
            r.appendChild(no);
        }
    }

}

var parser = document.createElement('a');
parser.href = document.URL;
if (parser.pathname == "/quizzer") {
    var t = new Trivia();
    document.getElementById('next_clue').addEventListener('click', function(e) {
        t.random();
2    });
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
    document.getElementById('correct').addEventListener('click', function() {
        t.correct();
    });
    document.getElementById('missed').addEventListener('click', function() {
        t.missed();
    });
    document.addEventListener('keypress', function(e) {
        switch (e.key) {
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
} else if (parser.pathname == "/search") {
    document.getElementById('search').addEventListener('keypress', function(e) {
        if (e.key == "Enter") {
            e.preventDefault();
            s = new Search(e.target.value);
            s.query(function(r) {
                s.to_html();
                s.named_entities();
            });
        }
    });
}
