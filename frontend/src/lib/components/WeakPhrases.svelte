<script lang="ts">
  import type { WeakPhrase } from '$lib/types';

  interface Props {
    phrases: WeakPhrase[];
  }

  let { phrases }: Props = $props();
</script>

<section class="rounded-xl border border-zinc-700/50 bg-zinc-800/30 p-6">
  <h3 class="mb-4 text-lg font-semibold text-zinc-100">Weak Phrases</h3>

  {#if phrases.length === 0}
    <p class="text-sm text-zinc-400">No weak phrases detected. Nice work!</p>
  {:else}
    <div class="space-y-3">
      {#each phrases as phrase, i}
        <div class="rounded-lg border border-zinc-700/30 bg-zinc-800/50 p-4">
          <div class="mb-2 flex items-start gap-3">
            <span class="mt-0.5 flex h-5 w-5 shrink-0 items-center justify-center rounded-full bg-amber-500/20 text-xs font-medium text-amber-400">
              {i + 1}
            </span>
            <div class="min-w-0 flex-1">
              <div class="mb-1 flex flex-wrap items-center gap-2">
                <span class="rounded bg-red-500/10 px-2 py-0.5 text-xs font-medium text-red-300 line-through decoration-red-400/50">
                  {phrase.original}
                </span>
                <svg class="h-4 w-4 shrink-0 text-zinc-500" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M13 7l5 5m0 0l-5 5m5-5H6" />
                </svg>
                <span class="rounded bg-emerald-500/10 px-2 py-0.5 text-xs font-medium text-emerald-300">
                  {phrase.suggestion}
                </span>
              </div>
              <p class="text-xs text-zinc-400">{phrase.reason}</p>
              {#if phrase.location}
                <p class="mt-1 text-xs text-zinc-500">Found in: {phrase.location}</p>
              {/if}
            </div>
          </div>
        </div>
      {/each}
    </div>
  {/if}
</section>
