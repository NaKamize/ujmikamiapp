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

interface ApiAboutItem {
  icon: string;
  title: string;
  text: string;
  order: number;
}

interface ApiPublication {
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
  const [publications, setPublications] = useState<ApiPublication[]>([]);
  const [aboutmeitems, setAboutMeItem] = useState<ApiAboutItem[]>([]);

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

    async function fetchPublications() {
      try {
        const response = await fetch(`${API_BASE_URL}/api/publications/`);
        if (!response.ok) {
          return;
        }

        const data: ApiPublication[] = await response.json();
        if (!isMounted || !Array.isArray(data) || data.length === 0) {
          return;
        }
        setPublications(data)
      } catch {
        // Keep static fallback if API is unavailable.
      }
    }

    async function fetchAboutMe() {
      try {
        const response = await fetch(`${API_BASE_URL}/api/about/`);
        if (!response.ok) {
          return;
        }

        const data: ApiAboutItem[] = await response.json();
        if (!isMounted || !Array.isArray(data) || data.length === 0) {
          return;
        }
        setAboutMeItem(data)
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
    fetchPublications();
    fetchMLModels();
    fetchAboutMe();
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
        items={aboutmeitems}
      />
      
      <Section 
        id="experience"
        className="section-gray"
        eyebrow="02 · Experience"
        title="Work Experiences"
        type="experience"
        experiences={experiences}
      />

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