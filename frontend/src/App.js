import React, { Component } from 'react';
import './index.css';
import {
  BrowserRouter as Router,
  Route,
  Link,
} from 'react-router-dom';
import 'purecss';
import axios from 'axios';

if (!process.env.NODE_ENV || process.env.NODE_ENV === 'development') {
  axios.defaults.baseURL = window.location.protocol + "//" + window.location.hostname + ":8000";
} else {
  axios.defaults.baseURL = window.location.protocol + "//" + window.location.hostname;
}

const WPM = 300;
class Question extends Component {
  constructor(props) {
    super(props);
    this.state = {
      len: 0,
      state: 0,
      buzzed: false
    };
  }
  tick = () => {
    if (this.state.state !== 0) {
      return;
    }
    const split = this.props.question.question.split(' ');
    if (this.state.len < this.props.question.question.split(' ').length + 3 * WPM / 60) {
      let weight = 1.0;
      if (this.state.len < 3) {
        weight *= 3 - this.state.len;
      } else if (this.state.len < split.length && (split[this.state.len].includes('.') || split[this.state.len].includes(','))) {
        weight *= 1.5;
      }
      if (/^[A-Z]/.test(split[this.state.len])) {
        weight *= 1.5;
      }
      if (this.state.len < split.length) {
        if (split[this.state.len].length <= 3) {
          weight *= 0.75;
        } else if (split[this.state.len].length >= 12) {
          weight *= 1.5;
        } else if (split[this.state.len].length >= 7) {
          weight *= 1.25;
        }
      }
      setTimeout(() => {
        if (this._ismounted) {
          this.setState({ "len": this.state.len + 1 });
          this.tick();
        }
      }, weight * 1000 * 60 / WPM);
    } else {
      this.setState({ "state": 2 });
    }
  }
  componentDidMount() {
    this._ismounted = true;
    document.addEventListener("keydown", this.onKey);
    this.tick();
  }
  buzz = () => {
    if (this.state.state < 2) {
      this.setState({ "state": this.state.state + 1 });
      this.setState({ "buzzed": true });
    } else if (this.state.buzzed === false) {
      this.refresh();
    }
  }
  refresh = () => {
    this.props.update();
    this.setState({ "state": 0 });
    this.setState({ "buzzed": false });
  }
  onKey = (event) => {
    console.log(event.keyCode);
    if (this._ismounted === false) {
      return;
    }
    if (event.keyCode === 32) {
      this.buzz();
    }
    if (this.state.state === 2) {
      if (event.keyCode === 49) {
        this.refresh();
      } else if (event.keyCode === 50) {
        this.refresh();
      }
    }
  }
  componentWillUnmount() {
    this._ismounted = false;
  }
  componentWillReceiveProps(nextProps) {
    this.setState({ len: 0 });
    this.setState({ state: 0 }, () => {
      this.tick();
    });
  }
  
  render() {
    const split = this.props.question.question.split(' ');
    const index = this.state.len < split.length ? this.state.len : split.length - 1;
    const q = split[index];
    let wrong_text = "Wrong";
    if (this.state.len < split.length) {
      wrong_text = "Neg";
    }
    let resp = (
      <div>
        <button onClick={this.refresh} className="pure-button">
          Continue (space)
        </button>
      </div>
    );
    if (this.state.buzzed) {
      resp = (
        <div>
          <button className="red pure-button" onClick={this.refresh}>{wrong_text} (1)</button>
          <button className="pure-button green" onClick={this.refresh}>Correct (2)</button>
        </div>
      );
    }
    return (
      <div>
        <button
          onClick={this.buzz}
          className={this.state.state < 2 ? 'show pure-button' : 'hidden'}>
          {this.state.state === 0 ? 'Buzz (space)' : 'Show (space)'}
          </button>
        <h3 className={this.state.state === 0 ? 'center' : 'hidden'}>{q}</h3>
        <div className={this.state.state === 2 ? 'show' : 'hidden'}>
          <div>{resp}</div>
          <p><strong>Answer:</strong> {this.props.question.answer}</p>
          <p className="right">{this.props.cat} | {this.props.diff}</p>
          <p>{this.props.question.question}</p>
        </div>
      </div>
    );
  }
}

class QuestionList extends Component {
  constructor(props) {
    super(props);
    this.state = {
      len: 0,
      questions: []
    };
  }
  refresh() {
    if (this.state.len <= 1) {
      axios.get(`/api/random/`)
        .then(res => {
          const results = res.data.results;
          this.setState({ "questions": results });
          this.setState({ "len": results.length });
        });
    }
  }
  componentWillMount() {
    this.refresh();
  }
  click = () => {
    this.setState({ "len": this.state.len - 1 });
    this.refresh();
  }
  render() {
    if (this.state.len === 0) {
      return (
        <p>Loading</p>
      );
    }
    const q = this.state.questions[this.state.len - 1];
    const question = q.question;
    //question.quesiton = question.question.replace('(*) ', '');
    return (
      <div>
        <p>{this.state.length}</p>
        <Question
          question={question}
          cat={q.get_category_display}
          diff={q.difficulty}
          update={this.click} />
      </div>
    );
  }
}
/*{this.state.questions.map((res, i) => <Question question={res.question} key={i}/> )}*/

const Practice = () => (
  <article className="pure-u-5-5 main-content">
    <QuestionList />
  </article>
);

const Home = () => (
  <article className="pure-u-5-5">
    <p>
      <strong>Kvizo</strong> is a practice and learning tool for adademic quiz bowl.
      It currently supports the following features:
    </p>
    <ul>
      <li>A practice interface designed to minimize eye movement.</li>
      <li>A question database.</li>
    </ul>
    <p>
      Kvizo is still in active development. This is an early preview release.
      The following are planned future features:
    </p>
    <ul>
      <li>User accounts.</li>
      <li>Tracking of performance over time.</li>
      <li>Exploration and searching insights for studying.</li>
      <li>Generated user profiles based on past performance.</li>
      <ul>
        <li>Estimated tossup points per tossup heard by category.</li>
        <li>Estimated probability of a user correctly answering a question.</li>
        <li>Personalized studying insights and suggestions.</li>
      </ul>
    </ul>
    <p>
      You can track Kvizo's development on <a href="https://github.com/carlcolglazier/kvizo">GitHub</a>. It was created as a reserach project by <a href="https://carlcolglazier.com/">Carl Colglazier</a>.
    </p>
  </article>
);

class App extends Component {
  render() {
    return (
      <Router>
        <main>
          <menu className="pure-menu pure-menu-horizontal">
            <ul className="pure-menu-list">
              <li className="pure-menu-item">
                <Link to="/" className="pure-menu-link pure-menu-heading">Kvizo</Link>
              </li>
              <li className="pure-menu-item">
                <Link to="/practice" className="pure-menu-link">Practice</Link>
              </li>
            </ul>
          </menu>
          <div className="pure-g">
            <Route exact path="/" component={Home} />
            <Route exact path="/practice" component={Practice} />
          </div>
        </main>
      </Router>
    );
  }
}

export default App;
