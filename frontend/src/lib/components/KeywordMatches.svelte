<script lang="ts">
  import type { KeywordMatch } from '$lib/types';

  interface Props {
    keywords: KeywordMatch[];
  }

  let { keywords }: Props = $props();

  let matched = $derived(keywords.filter((k) => k.found));
  let missing = $derived(keywords.filter((k) => !k.found));
  let matchRate = $derived(
    keywords.length > 0 ? Math.round((matched.length / keywords.length) * 100) : 0
  );
</script>

<section class="rounded-xl border border-zinc-700/50 bg-zinc-800/30 p-6">
  <div class="mb-4 flex items-center justify-between">
    <h3 class="text-lg font-semibold text-zinc-100">Keyword Analysis</h3>
    <span class="rounded-full bg-zinc-700/50 px-3 py-1 text-xs font-medium text-zinc-300">
      {matchRate}% match
    </span>
  </div>

  <!-- Match bar -->
  <div class="mb-5 h-2 overflow-hidden rounded-full bg-zinc-700">
    <div
      class="h-full rounded-full transition-all duration-700 ease-out {matchRate >= 70 ? 'bg-emerald-400' : matchRate >= 40 ? 'bg-amber-400' : 'bg-red-400'}"
      style="width: {matchRate}%"
    ></div>
  </div>

  <div class="grid gap-4 sm:grid-cols-2">
    <!-- Found -->
    <div>
      <h4 class="mb-2 text-xs font-medium uppercase tracking-wider text-emerald-400">
        Found ({matched.length})
      </h4>
      <div class="flex flex-wrap gap-2">
        {#each matched as kw}
          <span
            class="inline-flex items-center gap-1.5 rounded-md border border-emerald-500/20 bg-emerald-500/10 px-2.5 py-1 text-xs text-emerald-300"
            title={kw.context}
          >
            <svg class="h-3 w-3" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" />
            </svg>
            {kw.keyword}
          </span>
        {/each}
      </div>
    </div>

    <!-- Missing -->
    <div>
      <h4 class="mb-2 text-xs font-medium uppercase tracking-wider text-red-400">
        Missing ({missing.length})
      </h4>
      <div class="flex flex-wrap gap-2">
        {#each missing as kw}
          <span
            class="group relative inline-flex items-center gap-1.5 rounded-md border border-red-500/20 bg-red-500/10 px-2.5 py-1 text-xs text-red-300 cursor-help"
            title={kw.context}
          >
            <svg class="h-3 w-3" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd" />
            </svg>
            {kw.keyword}
          </span>
        {/each}
      </div>
    </div>
  </div>
</section>
