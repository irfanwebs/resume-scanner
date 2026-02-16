<script lang="ts">
  import type { Suggestion } from '$lib/types';

  interface Props {
    suggestions: Suggestion[];
  }

  let { suggestions }: Props = $props();

  const priorityStyles: Record<string, string> = {
    high: 'border-red-500/30 bg-red-500/10 text-red-300',
    medium: 'border-amber-500/30 bg-amber-500/10 text-amber-300',
    low: 'border-zinc-500/30 bg-zinc-500/10 text-zinc-300',
  };

  const categoryIcons: Record<string, string> = {
    impact: '🎯',
    keywords: '🔑',
    structure: '📐',
    formatting: '✨',
  };

  // Sort by priority: high first
  let sorted = $derived(
    [...suggestions].sort((a, b) => {
      const order = { high: 0, medium: 1, low: 2 };
      return (order[a.priority] ?? 3) - (order[b.priority] ?? 3);
    })
  );
</script>

<section class="rounded-xl border border-zinc-700/50 bg-zinc-800/30 p-6">
  <h3 class="mb-4 text-lg font-semibold text-zinc-100">Suggestions</h3>

  <div class="space-y-3">
    {#each sorted as suggestion}
      <div class="rounded-lg border border-zinc-700/30 bg-zinc-800/50 p-4">
        <div class="mb-2 flex items-center gap-2">
          <span class="text-base">{categoryIcons[suggestion.category] ?? '📝'}</span>
          <h4 class="flex-1 text-sm font-medium text-zinc-200">{suggestion.title}</h4>
          <span class="rounded-full border px-2 py-0.5 text-xs font-medium {priorityStyles[suggestion.priority] ?? ''}">
            {suggestion.priority}
          </span>
        </div>
        <p class="pl-7 text-sm text-zinc-400">{suggestion.description}</p>
      </div>
    {/each}
  </div>
</section>
