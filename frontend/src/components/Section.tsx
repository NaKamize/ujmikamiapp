import Card from './Card';
import Item from './Item';
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

type SectionType = 'cards' | 'about' | 'publications';

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
}

export default function Section({ id, title, lead, cards = [], items = [], publications = [], className, type, eyebrow }: SectionProps) {
  return (
    <section id={id} className={className}>
      <div className="container">
        {eyebrow && <span className="section-eyebrow">{eyebrow}</span>}
        <h2>{title}</h2>
        {lead && <p className="section-lead">{lead}</p>}

        {type === 'cards' && (
          <div className="cards-columns">
            {cards.map((c, i) => (
              <Card key={i} title={c.title} img={c.img} links={c.links} stat={c.stat}>{c.text}</Card>
            ))}
          </div>
        )}

        {type === 'about' && (
          <div className="about-items">
            {items.map((item, i) => (
              <Item key={i} icon={item.icon} img={item.img} title={item.title} text={item.text} />
            ))}
          </div>
        )}

        {type === 'publications' && (
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