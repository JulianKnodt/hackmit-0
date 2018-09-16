const React = require('react');
const base64 = require('base-64');
const src = "https://github.com/fivethirtyeight/russian-troll-tweets";

const clean = (str) => str.replace(/(?:https?|ftp):\/\/[\n\S]+/g, '');

export default class extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      tweet: "",
      similar: [],
      watson: null,
    };
  }
  async onClick() {
    const resp = await fetch(`http://localhost:5000/check?tweet=${this.state.tweet}`)
      .then(resp => resp.text());
    const data = JSON.parse(resp);
    this.setState({watson: data.classes[0].class_name, similar: []});
  }
  async related() {
    const resp = await fetch(`http://localhost:5000/approx?tweet=${this.state.tweet}`, {
    }).then(resp => resp.text());
    this.setState({similar: resp.split('\n').slice(1).filter(it => it).map(clean), watson: null})
  }
  onChange(e) {
    this.setState({tweet: e.target.value});
  }
  render() {
    return (<div style={{backgroundImage:
"url(https://cdn.downdetector.com/static/uploads/c/300/670d3/twitter-logo_7.png)", height: "100vh",
width:"100vw", backgroundRepeat: "no-repeat", backgroundPosition: "center"}}>
  <center style={{paddingTop:"300px"}}>
    {this.state.watson === null ? null :
      <h1>{Number(this.state.watson)*100}% Likely Fraudelent</h1>
    }
    {this.state.similar.map(tweet => {
      return <p>{tweet}</p>
    })}
    <font size="5">
    <p style={{paddingTop: this.state.similar.length ? "" : "300px"}}>How close is your tweet to <a href={src}>https://github.com/fivethirtyeight/russian-troll-tweets</a>?
    </p>
    </font>
    <textarea rows="4" cols="50" placeholder="Insert tweet here." id="userInput"
    onChange={this.onChange.bind(this)}>

    </textarea>
    <br/>
    <button onClick={this.onClick.bind(this)}>Check</button>
    <button onClick={this.related.bind(this)}>Similar</button>
  </center>
</div>)
  }
}
