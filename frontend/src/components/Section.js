import Card from './Card';

export default function Section({ id, title, lead, cards = [] }) {
  return (
    <section id={id} className="section-secondary">
      <div className="container">
        <h2>{title}</h2>
        {lead && <p className="section-lead">{lead}</p>}

        <div className="cards">
          {cards.map((c, i) => (
            <Card key={i} title={c.title}>{c.text}</Card>
          ))}
        </div>
      </div>
    </section>
  );
}