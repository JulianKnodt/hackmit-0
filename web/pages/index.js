const React = require('react');
const src = "https://github.com/fivethirtyeight/russian-troll-tweets";

const clean = (str) => str.replace(/(?:https?|ftp):\/\/[\n\S]+/g, '');

export default class extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      tweet: "",
      similar: [],
    };
  }
  onClick() {
    // TODO call api here
  }
  async related() {
    const resp = await fetch(`http://localhost:5000/approx?tweet=${this.state.tweet}`, {
    }).then(resp => resp.text());
    this.setState({similar: resp.split('\n').slice(1).filter(it => it).map(clean)});
  }
  onChange(e) {
    this.setState({tweet: e.target.value});
  }
  render() {
    return (<div style={{backgroundImage:
"url(https://cdn.downdetector.com/static/uploads/c/300/670d3/twitter-logo_7.png)", height: "100vh",
width:"100vw", backgroundRepeat: "no-repeat", backgroundPosition: "center"}}>
  <center style={{paddingTop:"300px"}}>
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
