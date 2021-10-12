import { action } from "@storybook/addon-actions";

import TagLabels from "@/components/TagLabels";

export default {
  title: "Components/Common/TagLabels",
  component: TagLabels,
  args: {
    tags: [
      { name: "Tag 1", colour: "#00AEC7", icon: "mdi-label" },
      { name: "Tag 2", colour: "#F44336", icon: "mdi-plus" },
      { name: "Tag with length > 20 characters", colour: "#4CAF50", icon: "mdi-pencil" },
    ],
  },
};

const Template = (args, { argTypes }) => ({
  components: { TagLabels },
  props: Object.keys(argTypes),
  methods: {
    onTagClick: action("tagClick"),
  },
  template: `
    <TagLabels v-bind="$props" @click:tag="onTagClick" />
  `,
});

export const Default = Template.bind({});
