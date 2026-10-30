content = open(r'harry-weapons.html', encoding='utf-8').read()
if 'gerudo-sword.png' in content and 'silver-lynel-horn.png' in content:
    print('SUCCESS')
else:
    print('FAIL - missing expected strings')
