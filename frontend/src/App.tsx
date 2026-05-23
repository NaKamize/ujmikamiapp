import './App.css';
import { useEffect, useState } from 'react';
import avatar from './assets/avatar.jpeg';
import azureImg from './assets/microsoft_azure.png';
import unetImg from './assets/UNet-En.png';
import grepolisImg from './assets/grepolisbot_preview.png';
import musicImg from './assets/music.png';
import Section from './components/Section';
import Footer from './components/Footer';
import Navbar from './components/Navbar';
import MLShowcase from './components/MLShowcase';
import WorkExperience, { WorkExperienceItem } from './components/WorkExperience';

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

interface ApiProject {
  id: number;
  title: string;
  description: string;
  image?: string | null;
  stat?: string;
  links?: Link[];
}

interface ApiExperience {
  id: number;
  company: string;
  role: string;
  period: string;
  location: string;
  description: string;
  current: boolean;
  order: number;
  technologies: { label: string }[];
}

interface ApiMLModel {
  id: number;
  title: string;
  description: string;
  category: string;
  category_display: string;
  architecture: string;
  framework: string;
  competition_name: string;
  competition_url: string;
  dataset_description: string;
  metrics: Record<string, number | string>;
  rank: string;
  score: string;
  image: string | null;
  links: Link[];
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

const skills: string[] = [
  'Formal Grammars', 'Music Informatics', 'Computer Vision',
  'Microsoft Azure', 'Information Systems', 'Python', 'Aerospace & Avionics',
];

/* Maps project titles from the API to local asset imports.
   When a project matches, the bundled asset is used instead of the API image URL. */
const PROJECT_IMAGES: Record<string, string> = {
  'Azure Data Pipelines & Infrastructure': azureImg,
  'U-Net Image Upscaling with Transfer Learning': unetImg,
  'GrepolisBot — Game Automation Userscript': grepolisImg,
  'Music Grammar Orchestrator': musicImg,
};

const API_BASE_URL = process.env.REACT_APP_API_BASE_URL ?? 'http://localhost:8000';

function normalizeImageUrl(img?: string | null): string | undefined {
  if (!img) {
    return undefined;
  }
  if (img.startsWith('http://') || img.startsWith('https://')) {
    return img;
  }
  return `${API_BASE_URL}${img}`;
}

const NAV_LINKS = [
  { id: 'about', label: 'About' },
  { id: 'experience', label: 'Experience' },
  { id: 'publications', label: 'Research' },
  { id: 'projects', label: 'Projects' },
  { id: 'ml-showcase', label: 'ML Showcase' },
];

function App() {
  const [apiProjectCards, setApiProjectCards] = useState<CardItem[]>([]);
  const [mlModels, setMlModels] = useState<ApiMLModel[]>([]);
  const [mlLoading, setMlLoading] = useState(true);
  const [mlError, setMlError] = useState<string | null>(null);
  const [experiences, setExperiences] = useState<WorkExperienceItem[]>([]);

  useEffect(() => {
    let isMounted = true;

    async function fetchExperiences() {
      try {
        const response = await fetch(`${API_BASE_URL}/api/experiences/`);
        if (!response.ok) return;

        const data: ApiExperience[] = await response.json();
        if (isMounted && Array.isArray(data) && data.length > 0) {
          setExperiences(data);
        }
      } catch {
        // Keep empty state if API is unavailable.
      }
    }

    async function fetchProjects() {
      try {
        const response = await fetch(`${API_BASE_URL}/api/projects/`);
        if (!response.ok) {
          return;
        }

        const data: ApiProject[] = await response.json();
        if (!isMounted || !Array.isArray(data) || data.length === 0) {
          return;
        }

        const mappedCards: CardItem[] = data.map((project) => ({
          title: project.title,
          text: project.description,
          img: PROJECT_IMAGES[project.title] ?? normalizeImageUrl(project.image),
          links: project.links,
          stat: project.stat,
        }));

        setApiProjectCards(mappedCards);
      } catch {
        // Keep static fallback if API is unavailable.
      }
    }

    async function fetchMLModels() {
      try {
        const response = await fetch(`${API_BASE_URL}/api/ml-models/`);
        if (!isMounted) return;

        if (!response.ok) {
          throw new Error(`Server responded with ${response.status}`);
        }

        const data: ApiMLModel[] = await response.json();
        if (isMounted) {
          if (Array.isArray(data) && data.length > 0) {
            setMlModels(data);
          }
          setMlLoading(false);
        }
      } catch (err) {
        if (isMounted) {
          setMlError(
            err instanceof Error ? err.message : 'Failed to load ML models'
          );
          setMlLoading(false);
        }
      }
    }

    fetchExperiences();
    fetchProjects();
    fetchMLModels();
    return () => {
      isMounted = false;
    };
  }, []);

  const displayedProjectCards = apiProjectCards.length > 0 ? apiProjectCards : [];

  return (
    <div className="App">
      <Navbar links={NAV_LINKS} />

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

      <section id="experience" className="section-gray">
        <div className="container">
          <span className="section-eyebrow">02 · Experience</span>
          <h2>Work Experience</h2>
          <p className="section-lead">
            Professional roles spanning aerospace software engineering, academic research, and full-stack development.
          </p>
          <WorkExperience experiences={experiences} />
        </div>
      </section>

      <Section
        id="publications"
        className="section-white"
        eyebrow="03 · Research"
        title="Research & Publications"
        lead="Academic work at the intersection of formal language theory and music informatics, covering my master's thesis and a peer-reviewed paper."
        type="publications"
        publications={publications}
      />

      <Section
        id="projects"
        className="section-gray"
        eyebrow="04 · Projects"
        title="Projects"
        lead="A selection of projects spanning game automation, computer vision, cloud infrastructure, and aerospace software."
        type="cards"
        cards={displayedProjectCards}
      />

      <MLShowcase
        models={mlModels}
        loading={mlLoading}
        error={mlError}
      />

      <Footer />
    </div>
  );
}

export default App;