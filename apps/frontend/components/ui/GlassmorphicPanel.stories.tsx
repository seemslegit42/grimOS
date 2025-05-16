import type { Meta, StoryObj } from '@storybook/react';

import { GlassmorphicPanel } from './GlassmorphicPanel';

// More on how to set up stories at: https://storybook.js.org/docs/writing-stories#default-export
const meta = {
  title: 'UI/GlassmorphicPanel',
  component: GlassmorphicPanel,
  parameters: {
    // Optional parameter to center the component in the Storybook canvas
    layout: 'centered',
  },
  // This component will have an automatically generated Autodocs entry: https://storybook.js.org/docs/writing-docs/autodocs
  tags: ['autodocs'],
  // More on argTypes: https://storybook.js.org/docs/api/argtypes
  argTypes: {
    // Define control types for props here if needed
  },
} satisfies Meta<typeof GlassmorphicPanel>;

export default meta;
type Story = StoryObj<typeof meta>;

// More on writing stories with args: https://storybook.js.org/docs/writing-stories#play-function
export const Primary: Story = {
  args: {
    children: (
      <div>
        <p>This is a glassmorphic panel.</p>
        <p>It can contain various elements.</p>
      </div>
    ),
  },
};