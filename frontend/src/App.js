import './App.css';
import avatar from './assets/background.jpeg';
import Section from './components/Section';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <img className="avatar" src={avatar} alt="Profilová fotografia" />
        <h1>Jozef Makiš</h1>
        <p className="lead">Fullstack developer • počítačové videnie (Computer Vision)</p>

        <div className="actions">
          <a className="btn" href="https://www.linkedin.com/in/jozef-maki%C5%A1-05a406251/" title="LinkedIn" target="_blank" rel="noopener noreferrer">LinkedIn</a>
          <a className="btn" href="https://github.com/NaKamize" title="Portfolio">Portfolio</a>
          <a className="btn outline" href="mailto:makisjozef28@gmail.com" title="Kontakt">Kontaktovať</a>
        </div>

        <p className="skills">Computer Vision · React · Node.js · Python</p>
      </header>

      <Section
       id="about"
       title="O mne"
       lead="Som fullstack developer, zaujímam sa o teóriu a hudbu. Pracujem na projektoch z computer vision a webu."
       cards={[
         { title: 'Projekty', text: 'Open-source a osobné projekty — React, Node.js, CV.' },
         { title: 'Výskum', text: 'Teoretické aspekty strojového učenia a počítačového videnia.' },
         { title: 'Hudba', text: 'Komponovanie a produkcia — voľný čas a inšpirácia.' },
       ]}
       />
    </div>
  );
}

export default App;
