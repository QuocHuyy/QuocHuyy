import sys,glob
from PIL import Image
files=sys.argv[2:];out=sys.argv[1];cols=min(6,len(files));w,h=360,640
rows=(len(files)+cols-1)//cols;S=Image.new('RGB',(cols*w,rows*h),(40,40,40))
for i,f in enumerate(files):S.paste(Image.open(f).convert('RGB').resize((w,h),Image.LANCZOS),((i%cols)*w,(i//cols)*h))
S.save(out)
