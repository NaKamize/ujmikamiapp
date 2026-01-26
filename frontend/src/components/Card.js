import './Card.css';

export default function Card({ title, children, img }) {
  return (
    <div className="card">
      <h3>{title}</h3>
      <p>{children}</p>
      <div>
        <img src={img} alt="" />
      </div>
    </div>
  );
}