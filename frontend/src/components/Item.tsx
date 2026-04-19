import './Item.css';

interface ItemProps {
  title: string;
  text: string;
  img?: string;
  icon?: string;
}

export default function Item({ img, title, text, icon }: ItemProps) {
  return (
    <div className="about-item">
      {icon && <span className="about-item-icon">{icon}</span>}
      {img && <img src={img} alt={title} className="about-img" />}
      <h2>{title}</h2>
      <p>{text}</p>
    </div>
  );
}