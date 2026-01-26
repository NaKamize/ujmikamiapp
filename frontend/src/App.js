import './App.css';
import avatar from './assets/background.jpeg';
import Section from './components/Section';

function App() {
  return (
    <div className="App">
      <header className="App-header-modern">
        <div className="header-card">
          <img className="avatar-modern" src={avatar} alt="Jozef Makiš" />
          <h1>Jozef Makiš</h1>
          <p className="lead">Fullstack developer • Computer Vision</p>
          <div className="actions-modern">
            <a className="btn-modern" href="https://www.linkedin.com/in/jozef-maki%C5%A1-05a406251/" title="LinkedIn" target="_blank" rel="noopener noreferrer">
              <span>LinkedIn</span>
            </a>
            <a className="btn-modern" href="https://github.com/NaKamize" title="Portfolio">
              <span>Portfolio</span>
            </a>
            <a className="btn-modern outline" href="mailto:makisjozef28@gmail.com" title="Contact">
              <span>Contact</span>
            </a>
          </div>
          <p className="skills-modern">
            Formal Grammars · Music Informatics · Computer Vision · Microsoft Azure · Information Systems · Python · Aerospace & Avionics
          </p>
        </div>
      </header>
      <div className="header-wave">
        <svg viewBox="0 0 1440 320" width="100%" height="120" preserveAspectRatio="none">
          <path
            fill="#fff"
            fillOpacity="1"
            d="M0,224L48,197.3C96,171,192,117,288,117.3C384,117,480,171,576,186.7C672,203,768,181,864,154.7C960,128,1056,96,1152,101.3C1248,107,1344,149,1392,170.7L1440,192L1440,320L1392,320C1344,320,1248,320,1152,320C1056,320,960,320,864,320C768,320,672,320,576,320C480,320,384,320,288,320C192,320,96,320,48,320L0,320Z"
          ></path>
        </svg>
      </div>

      <Section
        id="mypro"
        title="My Projects"
        lead="Here you can find a selection of my projects and experiences. My journey started with academic research in grammar in music and grammar systems, continued through computer vision, and led to practical experience with cloud and information systems, as well as Python scripting for aerospace and avionics."
        cards={[
          {
            title: "Academic Background",
            text: "I hold a Master's and Bachelor's degree focused on grammar in music and grammar systems. My studies involved formal systems, pattern recognition, and the intersection of music and computational linguistics.",
            img: null,
          },
          {
            title: "Computer Vision",
            text: "I have a strong background in computer vision, working on object tracking, image analysis, and developing advanced models for visual data processing.",
            img: null,
          },
          {
            title: "Work Experience",
            text: "I have hands-on experience with Microsoft Azure and have developed an information system for a school. My work included cloud deployment, backend development, and system integration.",
            img: null,
          },
          {
            title: "Python Scripting for Aerospace & Avionics",
            text: "I write Python scripts and system tests for aerospace and avionics applications, focusing on automation, reliability, and safety-critical systems.",
            img: null,
          },
        ]}
      />
    </div>
  );
}

export default App;