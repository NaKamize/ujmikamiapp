import Card from './Card';
import Item from './Item';
import WorkExperience from './WorkExperience';
import './Sections.css';

interface Link {
  label: string;
  url: string;
}

interface CardItem {
  title: string;
  text: string;
  img?: string;
  links?: Link[];
  stat?: string;
}

interface AboutItem {
  title: string;
  text: string;
  img?: string;
  icon?: string;
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

interface TechBadge {
  label: string;
}

interface Experience {
  id: number;
  company: string;
  role: string;
  period: string;
  location: string;
  description: string;
  technologies: TechBadge[];
  current?: boolean;
}

type SectionType = 'cards' | 'about' | 'publications' | 'experience';

interface SectionProps {
  id: string;
  title: string;
  className?: string;
  type: SectionType;
  lead?: string;
  eyebrow?: string;
  cards?: CardItem[];
  items?: AboutItem[];
  publications?: Publication[];
  experiences?: Experience[];
  loading?: boolean;
  error?: string | null;
}

export default function Section({ id, title, lead, cards = [], items = [], publications = [], experiences = [], className, type, eyebrow, loading = false, error = null }: SectionProps) {
  return (
    <section id={id} className={className}>
      <div className="container">
        {eyebrow && <span className="section-eyebrow">{eyebrow}</span>}
        <h2>{title}</h2>
        {lead && <p className="section-lead">{lead}</p>}

        {loading && (
          <div className="section-loading" role="status" aria-live="polite">
            Loading content. Backend may be waking up from cold start...
          </div>
        )}

        {!loading && error && (
          <div className="section-error" role="status" aria-live="polite">
            We could not load this section yet ({error}). Backend may still be starting. Please refresh in a few seconds.
          </div>
        )}

        {!loading && !error && type === 'cards' && (
          <div className="cards-columns">
            {cards.map((c, i) => (
              <Card key={i} title={c.title} img={c.img} links={c.links} stat={c.stat}>{c.text}</Card>
            ))}
          </div>
        )}

        {!loading && !error && type === 'about' && (
          <div className="about-items">
            {items.map((item, i) => (
              <Item key={i} icon={item.icon} img={item.img} title={item.title} text={item.text} />
            ))}
          </div>
        )}

        {!loading && !error && type === 'experience' && (
            <WorkExperience experiences={experiences} />
        )}

        {!loading && !error && type === 'publications' && (
          <div className="publications-list">
            {publications.map((pub, i) => (
              <div key={i} className="pub-card">
                <span className="pub-badge">{pub.badge}</span>
                <div className="pub-body">
                  <h3 className="pub-title">{pub.title}</h3>
                  {pub.subtitle && <p className="pub-subtitle">{pub.subtitle}</p>}
                  <p className="pub-authors">{pub.authors}</p>
                  <p className="pub-venue">{pub.venue}</p>
                  {pub.description && <p className="pub-desc">{pub.description}</p>}
                  <div className="pub-links">
                    {pub.links && pub.links.map((l, j) => (
                      <a key={j} href={l.url} className="pub-link" target="_blank" rel="noopener noreferrer">{l.label}</a>
                    ))}
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </section>
  );
}