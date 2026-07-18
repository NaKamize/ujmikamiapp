import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import ChatWidget from './ChatWidget';

describe('ChatWidget', () => {
  test('panel is closed by default and opens when the FAB is clicked', async () => {
    render(<ChatWidget />);

    const panel = screen.getByText(/ask about jozef's work/i).closest('.chat-widget__panel');
    expect(panel).not.toHaveClass('chat-widget__panel--open');

    await userEvent.click(screen.getByRole('button', { name: /open chat/i }));

    expect(panel).toHaveClass('chat-widget__panel--open');
  });

  test('shows the offline fallback message when no AI service URL is configured', async () => {
    render(<ChatWidget />);

    await userEvent.click(screen.getByRole('button', { name: /open chat/i }));
    await userEvent.type(screen.getByPlaceholderText(/ask a question/i), "What is Jozef's background?");
    await userEvent.click(screen.getByRole('button', { name: /send/i }));

    expect(await screen.findByText(/currently offline/i)).toBeInTheDocument();
  });
});
