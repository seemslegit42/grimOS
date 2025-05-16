import type { Meta, StoryObj } from '@storybook/react';
import { GlassmorphicCard } from './GlassmorphicCard'; // Assuming GlassmorphicCard is in the same directory

const meta: Meta<typeof GlassmorphicCard> = {
  title: 'UI/GlassmorphicCard',
  component: GlassmorphicCard,
  tags: ['autodocs'],
  argTypes: {
    // Define any control types for props here if needed
  },
};

export default meta;
type Story = StoryObj<typeof GlassmorphicCard>;

export const Primary: Story = {
  args: {
    title: 'Hello, Glassmorphic Card!',
    children: (
      <div>
        <p>This is some sample content inside the glassmorphic card.</p>
        <p>It demonstrates how content is rendered within the card's body.</p>
      </div>
    ),
  },
};