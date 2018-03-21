import os, requests
import threading
import urllib2
import time

URL = "https://scontent-yyz1-1.cdninstagram.com/vp/2099048b4b856d52317eb5b27553d9f8/5AB5536F/t50.2886-16/27297476_183429395760961_8423015983735635968_n.mp4"

# Creates a range of byte values if needed
def buildRange(value, splits):
    range= []
    for i in range(splits):
        if i == 0:
            lst.append('%s-%s' % (i, int(round(1 + i * value/(splits*1.0) + value/(splits*1.0)-1, 0))))
        else:
            lst.append('%s-%s' % (int(round(1 + i * value/(numSplits*1.0),0)), int(round(1 + i * value/(splits*1.0) + value/(splits*1.0)-1, 0))))
    return range

def main(url=None, chunks=8):
    start_time = time.time()
    if not url:
        print "Please provide a URL to begin download"
        return

    # Get the file name    
    fileName = url.split('/')[-1]

    # Check if server supports byte range
    #@TODO - Add here

    # Get the file size
    sizeInBytes = requests.head(url, headers={'Accept-Encoding': 'identity'}).headers.get('content-length', None)

    print "%s bytes to download." % sizeInBytes
    if not sizeInBytes:
        print "Size cannot be determined."
        return

    # Structure to store the data, Each entry will contain a chunk
    downloaded = {}

    # split total num bytes into ranges
    ranges = buildRange(int(sizeInBytes), chunks)

    # Define our downloader method
    def downloadChunk(chunkNum, irange):
        req = urllib2.Request(url)
        req.headers['Range'] = 'bytes={}'.format(irange)
        downloaded[chunkNum] = urllib2.urlopen(req).read()

    # create one downloading thread per chunk
    downloaders = [
        threading.Thread(
            target=downloadChunk, 
            args=(chunkNum, irange),
        )
        for chunkNum,irange in enumerate(ranges)
        ]

    print 'Downloading...'

    # Run threads in parallel to download file
    for th in downloaders:
        th.start()
    time.sleep(10)
    print(downloaded.values())
    for th in downloaders:
        th.join()

    # Download Complete 
    print 'done: got {} chunks, total {} bytes'.format(
        len(downloaded), sum((len(chunk) for chunk in downloaded.values()))
    )

    print "--- %s seconds ---" % str(time.time() - start_time)

    if os.path.exists(fileName):
        os.remove(fileName)
    # reassemble file in correct order
    with open(fileName, 'w') as fh:
        for _idx,chunk in sorted(downloaded.iteritems()):
            fh.write(chunk)

    print "Finished Writing file %s" % fileName
    print 'file size {} bytes'.format(os.path.getsize(fileName))

def verifyFile(fileName, hash)
    BLOCKSIZE = 65536
    hasher = hashlib.md5()
    with open(fileName, 'rb') as afile:
        buf = afile.read(BLOCKSIZE)
        while len(buf) > 0:
            hasher.update(buf)
            buf = afile.read(BLOCKSIZE)
    print(hasher.hexdigest())

if __name__ == '__main__':
    main(URL)