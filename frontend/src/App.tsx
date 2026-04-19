import './App.css';
import avatar from './assets/avatar.jpeg';
import plane from './assets/plane.jpg';
import unet from './assets/mozaika_next.png';
import azure_logo from './assets/microsoft_azure.png';
import Section from './components/Section';
import Footer from './components/Footer';

interface Link {
  label: string;
  url: string;
}

interface AboutItem {
  icon: string;
  title: string;
  text: string;
}

interface Publication {
  badge: string;
  title: string;
  subtitle?: string;
  authors: string;
  venue: string;
  description?: string;
  links?: Link[];
}

interface CardItem {
  title: string;
  text: string;
  img?: string;
  links?: Link[];
  stat?: string;
}

const aboutItems: AboutItem[] = [
  {
    icon: '\u{1F9D1}\u200D\u{1F4BB}',
    title: 'Who am I?',
    text: "I'm a Slovak software developer with a background in computer science research, currently working in aerospace and avionics. I build things: research prototypes, automation scripts, full-stack applications and cloud systems.",
  },
  {
    icon: '\u{1F393}',
    title: 'Education',
    text: "Master's degree (Ing.) from the Faculty of Information Technology, Brno University of Technology (VUT FIT). My studies covered formal grammars, music informatics, machine learning, computer vision and AI. My thesis sits at the intersection of formal language theory and computational musicology.",
  },
  {
    icon: '\u{1F3B5}',
    title: 'Interests',
    text: 'Music informatics, computer vision, formal language theory, game automation, aerospace & avionics systems, and building tools that make repetitive work disappear.',
  },
];

const publications: Publication[] = [
  {
    badge: "IT SPY 2025",
    title: "Výpočetná muzikológia: modely, metódy a aplikácie",
    subtitle: "Computational Musicology: Models, Methods and Applications",
    authors: "Jozef Makiš, supervised by prof. RNDr. Alexandr Meduna, CSc.",
    venue: "VUT FIT Brno · IT SPY 2025 competition (best student IT projects in CZ & SK)",
    description:
      "Master's thesis selected for the IT SPY competition. The work explores the intersection of formal grammar systems and music theory, defining models and methods for computational musicology: parsing symbolic music and generating orchestrations using multi-generative grammar systems.",
    links: [
      { label: "IT SPY entry", url: "https://www.itspy.cz/sk/thesis/vypocetna-muzikologia-modely-metody-a-aplikacie/" },
    ],
  },
  {
    badge: "arXiv 2025",
    title: "Orchestration of Music by Grammar Systems",
    authors: "Jozef Makiš, Alexander Meduna, Zbyněk Křivka · VUT FIT Brno",
    venue: "EPTCS 422, 2025, pp. 45–58 · Formal Languages & Automata Theory (cs.FL)",
    description:
      "We define multi-generative rule-synchronized scattered-context grammar systems (without erasing rules) and demonstrate how to simultaneously arrange a musical composition for a full orchestra consisting of several instruments. Classical and jazz orchestration examples are provided, followed by five open problem areas related to this approach.",
    links: [
      { label: "arXiv:2507.15314", url: "https://arxiv.org/abs/2507.15314" },
      { label: "PDF", url: "https://arxiv.org/pdf/2507.15314" },
      { label: "DOI 10.4204/EPTCS.422.4", url: "https://doi.org/10.4204/EPTCS.422.4" },
    ],
  },
];

const projectCards: CardItem[] = [
  {
    title: "GrepolisBot",
    text: "A Tampermonkey userscript for the browser game Grepolis that automates farm collection, culture events and attack dodging. Built with a modern JS workflow (esbuild, ESLint, Prettier). The control panel is draggable and persists settings across page refreshes.",
    stat: "63+ installs on GreasyFork",
    links: [
      { label: "GreasyFork", url: "https://greasyfork.org/en/scripts/468760-grepolisbot" },
      { label: "GitHub", url: "https://github.com/NaKamize/GrepolisBot" },
    ],
  },
  {
    title: "Computer Vision",
    text: "Object tracking, image segmentation and visual analysis, including work on advanced U-Net-based models for image processing and real-world inspection tasks.",
    img: unet,
  },
  {
    title: "Cloud & Information Systems",
    text: "Hands-on experience with Microsoft Azure: cloud deployment, backend development, and building a school information system with full system integration.",
    img: azure_logo,
  },
  {
    title: "Aerospace & Avionics",
    text: "Python scripting and system tests for safety-critical aerospace and avionics applications, focusing on automation, reliability, and compliance with industry standards.",
    img: plane,
  },
];

const skills: string[] = [
  'Formal Grammars', 'Music Informatics', 'Computer Vision',
  'Microsoft Azure', 'Information Systems', 'Python', 'Aerospace & Avionics',
];

function App() {
  return (
    <div className="App">
      <header className="hero">
        <div className="hero-glow" />
        <div className="hero-content">
          <div className="avatar-ring">
            <img src={avatar} alt="Jozef Makiš" />
          </div>
          <h1 className="hero-name">Jozef Makiš</h1>
          <p className="hero-lead">Fullstack Developer · Computer Vision · Music Informatics</p>
          <div className="hero-actions">
            <a className="btn-primary" href="https://www.linkedin.com/in/jozef-maki%C5%A1-05a406251/" target="_blank" rel="noopener noreferrer">LinkedIn</a>
            <a className="btn-primary" href="https://github.com/NaKamize" target="_blank" rel="noopener noreferrer">GitHub</a>
            <a className="btn-outline" href="mailto:makisjozef28@gmail.com">Contact</a>
          </div>
          <div className="hero-tags">
            {skills.map(s => <span key={s} className="hero-tag">{s}</span>)}
          </div>
        </div>
      </header>

      <div className="hero-wave">
        <svg viewBox="0 0 1440 80" width="100%" height="80" preserveAspectRatio="none" aria-hidden="true">
          <path fill="#ffffff" d="M0,32 C240,72 720,8 960,44 C1200,72 1340,24 1440,36 L1440,80 L0,80 Z" />
        </svg>
      </div>

      <Section
        id="about"
        className="section-white"
        eyebrow="01 · About"
        title="About Me"
        type="about"
        items={aboutItems}
      />

      <Section
        id="publications"
        className="section-gray"
        eyebrow="02 · Research"
        title="Research & Publications"
        lead="Academic work at the intersection of formal language theory and music informatics, covering my master's thesis and a peer-reviewed paper."
        type="publications"
        publications={publications}
      />

      <Section
        id="projects"
        className="section-white"
        eyebrow="03 · Projects"
        title="Projects"
        lead="A selection of projects spanning game automation, computer vision, cloud infrastructure, and aerospace software."
        type="cards"
        cards={projectCards}
      />

      <Footer />
    </div>
  );
}

export default App;