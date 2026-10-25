#!/usr/bin/env bash
# ───────────────────────────────────────────────────────────
# post-upgrade-antigravity.sh
# Áp dụng Antigravity (Gemini CLI) host vào gstack sau mỗi lần upgrade.
# Lưu tại ~/.gstack/hooks/ — KHÔNG bị ghi đè khi upgrade.
# Idempotent — chạy bao nhiêu lần cũng an toàn.
#
# Cách dùng: bash ~/.gstack/hooks/post-upgrade-antigravity.sh
# ───────────────────────────────────────────────────────────
set -euo pipefail

# Tìm gstack source
GSTACK_DIR=""
for d in "$HOME/.gemini/config/skills" "$HOME/.gstack/repos/gstack"; do
  [ -d "$d/hosts" ] && GSTACK_DIR="$d" && break
done
[ -z "$GSTACK_DIR" ] && echo "❌ Không tìm thấy gstack source" >&2 && exit 1

export GSTACK_DIR
VER=$(cat "$GSTACK_DIR/VERSION" 2>/dev/null || echo "unknown")
echo "🔧 Patching gstack v$VER tại $GSTACK_DIR"

# ─── 1. Tạo hosts/antigravity.ts ─────────────────────────
cat > "$GSTACK_DIR/hosts/antigravity.ts" << 'EOF'
import type { HostConfig } from '../scripts/host-config';

const antigravity: HostConfig = {
  name: 'antigravity',
  displayName: 'Antigravity (Gemini CLI)',
  cliCommand: 'gemini',
  cliAliases: ['antigravity'],

  globalRoot: '.gemini/skills/gstack',
  localSkillRoot: '.gemini/skills/gstack',
  hostSubdir: '.gemini',
  usesEnvVars: true,

  frontmatter: {
    mode: 'allowlist',
    keepFields: ['name', 'description'],
    descriptionLimit: null,
  },

  generation: {
    generateMetadata: false,
    skipSkills: ['codex'],
  },

  pathRewrites: [
    { from: '~/.claude/skills/gstack', to: '~/.gemini/skills/gstack' },
    { from: '.claude/skills/gstack', to: '.gemini/skills/gstack' },
    { from: '.claude/skills', to: '.gemini/skills' },
    { from: '~/.codex/skills/gstack', to: '~/.gemini/skills/gstack' },
    { from: '.codex/skills', to: '.gemini/skills' },
  ],

  suppressedResolvers: ['GBRAIN_CONTEXT_LOAD', 'GBRAIN_SAVE_RESULTS'],

  runtimeRoot: {
    globalSymlinks: ['bin', 'browse/dist', 'browse/bin', 'gstack-upgrade', 'ETHOS.md'],
    globalFiles: {
      'review': ['checklist.md', 'TODOS-format.md'],
    },
  },

  install: {
    prefixable: false,
    linkingStrategy: 'symlink-generated',
  },

  learningsMode: 'basic',
};

export default antigravity;
EOF
echo "  ✅ hosts/antigravity.ts"

# ─── 2. Patch hosts/index.ts ─────────────────────────────
if ! grep -q "antigravity" "$GSTACK_DIR/hosts/index.ts" 2>/dev/null; then
  python3 -c "
import os
path = os.path.join(os.environ['GSTACK_DIR'], 'hosts', 'index.ts')
with open(path) as f:
    c = f.read()
c = c.replace(\"import gbrain from './gbrain';\", \"import gbrain from './gbrain';\\nimport antigravity from './antigravity';\")
c = c.replace('hermes, gbrain]', 'hermes, gbrain, antigravity]')
c = c.replace('hermes, gbrain }', 'hermes, gbrain, antigravity }')
with open(path, 'w') as f:
    f.write(c)
print('  ✅ hosts/index.ts — patched')
"
else
  echo "  ✅ hosts/index.ts — đã có"
fi

# ─── 3+4. Patch setup script (args + install block) ──────
if ! grep -q "INSTALL_ANTIGRAVITY" "$GSTACK_DIR/setup" 2>/dev/null; then
  python3 -c "
import os, sys, re
path = os.path.join(os.environ['GSTACK_DIR'], 'setup')
with open(path) as f:
    c = f.read()

# 3a. Error messages
c = re.sub(r'kiro,\s*', 'kiro, antigravity, ', c)

# 3b. Case validation
c = re.sub(r'claude\|codex\|kiro\|', 'claude|codex|kiro|antigravity|gemini|', c)

# 3c. INSTALL flag
c = c.replace('INSTALL_KIRO=0\n', 'INSTALL_KIRO=0\nINSTALL_ANTIGRAVITY=0\n')

# 3d. Normalize gemini alias
c = c.replace(
    'if [ \"\$HOST\" = \"auto\" ]; then\n',
    'if [ \"\$HOST\" = \"gemini\" ]; then HOST=\"antigravity\"; fi\nif [ \"\$HOST\" = \"auto\" ]; then\n'
)

# 3e. Auto-detect
c = c.replace(
    'command -v kiro-cli >/dev/null 2>&1 && INSTALL_KIRO=1\n',
    'command -v kiro-cli >/dev/null 2>&1 && INSTALL_KIRO=1\n  command -v gemini >/dev/null 2>&1 && INSTALL_ANTIGRAVITY=1\n'
)

# 3f. None-found check
c = c.replace(
    '[ \"\$INSTALL_KIRO\" -eq 0 ] && [ \"\$INSTALL_FACTORY\"',
    '[ \"\$INSTALL_KIRO\" -eq 0 ] && [ \"\$INSTALL_ANTIGRAVITY\" -eq 0 ] && [ \"\$INSTALL_FACTORY\"'
)

# 3g. Explicit host flag
c = c.replace(
    'elif [ \"\$HOST\" = \"factory\" ]; then\n  INSTALL_FACTORY=1',
    'elif [ \"\$HOST\" = \"antigravity\" ]; then\n  INSTALL_ANTIGRAVITY=1\nelif [ \"\$HOST\" = \"factory\" ]; then\n  INSTALL_FACTORY=1'
)

# 4. Install block (chèn trước Section 7)
install_block = '''
# 6d. Install for Antigravity / Gemini CLI (copy from .agents/skills, rewrite paths)
if [ \"\$INSTALL_ANTIGRAVITY\" -eq 1 ]; then
  ANTIGRAVITY_SKILLS=\"\$HOME/.gemini/skills\"
  AGENTS_DIR=\"\$SOURCE_GSTACK_DIR/.agents/skills\"
  mkdir -p \"\$ANTIGRAVITY_SKILLS\"
  ANTIGRAVITY_GSTACK=\"\$ANTIGRAVITY_SKILLS/gstack\"
  [ -L \"\$ANTIGRAVITY_GSTACK\" ] && rm -f \"\$ANTIGRAVITY_GSTACK\"
  mkdir -p \"\$ANTIGRAVITY_GSTACK\" \"\$ANTIGRAVITY_GSTACK/browse\" \"\$ANTIGRAVITY_GSTACK/gstack-upgrade\" \"\$ANTIGRAVITY_GSTACK/review\"
  _link_or_copy \"\$SOURCE_GSTACK_DIR/bin\" \"\$ANTIGRAVITY_GSTACK/bin\"
  _link_or_copy \"\$SOURCE_GSTACK_DIR/browse/dist\" \"\$ANTIGRAVITY_GSTACK/browse/dist\"
  _link_or_copy \"\$SOURCE_GSTACK_DIR/browse/bin\" \"\$ANTIGRAVITY_GSTACK/browse/bin\"
  if [ -f \"\$SOURCE_GSTACK_DIR/ETHOS.md\" ]; then
    _link_or_copy \"\$SOURCE_GSTACK_DIR/ETHOS.md\" \"\$ANTIGRAVITY_GSTACK/ETHOS.md\"
  fi
  if [ -f \"\$AGENTS_DIR/gstack-upgrade/SKILL.md\" ]; then
    _link_or_copy \"\$AGENTS_DIR/gstack-upgrade/SKILL.md\" \"\$ANTIGRAVITY_GSTACK/gstack-upgrade/SKILL.md\"
  fi
  for f in checklist.md design-checklist.md greptile-triage.md TODOS-format.md; do
    if [ -f \"\$SOURCE_GSTACK_DIR/review/\$f\" ]; then
      _link_or_copy \"\$SOURCE_GSTACK_DIR/review/\$f\" \"\$ANTIGRAVITY_GSTACK/review/\$f\"
    fi
  done
  sed -e \"s|~/.claude/skills/gstack|~/.gemini/skills/gstack|g\" \\\\
      -e \"s|\\\\.claude/skills/gstack|.gemini/skills/gstack|g\" \\\\
      -e \"s|\\\\.claude/skills|.gemini/skills|g\" \\\\
      \"\$SOURCE_GSTACK_DIR/SKILL.md\" > \"\$ANTIGRAVITY_GSTACK/SKILL.md\"
  if [ ! -d \"\$AGENTS_DIR\" ]; then
    echo \"  warning: no .agents/skills/ directory found\" >&2
  else
    for skill_dir in \"\$AGENTS_DIR\"/gstack*/; do
      [ -f \"\$skill_dir/SKILL.md\" ] || continue
      skill_name=\"\$(basename \"\$skill_dir\")\"
      target_dir=\"\$ANTIGRAVITY_SKILLS/\$skill_name\"
      mkdir -p \"\$target_dir\"
      sed -e 's|\\\\\\$HOME/.codex/skills/gstack|\\$HOME/.gemini/skills/gstack|g' \\\\
          -e \"s|~/.codex/skills/gstack|~/.gemini/skills/gstack|g\" \\\\
          -e \"s|~/.claude/skills/gstack|~/.gemini/skills/gstack|g\" \\\\
          \"\$skill_dir/SKILL.md\" > \"\$target_dir/SKILL.md\"
      if [ -d \"\$skill_dir/sections\" ]; then
        mkdir -p \"\$target_dir/sections\"
        for section_file in \"\$skill_dir/sections\"/*; do
          [ -f \"\$section_file\" ] || continue
          sed -e 's|\\\\\\$HOME/.codex/skills/gstack|\\$HOME/.gemini/skills/gstack|g' \\\\
              -e \"s|~/.codex/skills/gstack|~/.gemini/skills/gstack|g\" \\\\
              -e \"s|~/.claude/skills/gstack|~/.gemini/skills/gstack|g\" \\\\
              \"\$section_file\" > \"\$target_dir/sections/\$(basename \"\$section_file\")\"
        done
      fi
    done
    echo \"gstack ready (antigravity).\"
    echo \"  antigravity skills: \$ANTIGRAVITY_SKILLS\"
  fi
fi

'''
marker = '# 7. Create .agents/'
if marker in c:
    c = c.replace(marker, install_block + marker)

with open(path, 'w') as f:
    f.write(c)
print('  ✅ setup — patched (args + auto-detect + install block)')
"
else
  echo "  ✅ setup — đã có"
fi

# ─── 5. Chạy setup ───────────────────────────────────────
echo ""
echo "🚀 Chạy ./setup --host antigravity -q ..."
cd "$GSTACK_DIR"
./setup --host antigravity -q 2>&1

echo ""
echo "🎉 Hoàn tất! Antigravity gstack v$VER đã sẵn sàng."
echo "   Skills: ~/.gemini/skills/"
