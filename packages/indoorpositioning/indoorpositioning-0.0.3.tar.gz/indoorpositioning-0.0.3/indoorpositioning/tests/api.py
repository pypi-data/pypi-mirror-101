from indoorpositioning import IndoorPositioning
from indoorpositioning.scanner import OSXWifiScanner
from sklearn.ensemble import RandomForestClassifier
from time import sleep


if __name__ == '__main__':
    positioning = IndoorPositioning(scanner=OSXWifiScanner())
    positioning.load_from('data/home.json')
    clf = positioning.fit(RandomForestClassifier(n_estimators=5))
    print('Self score %.2f' % clf.score(positioning.X, positioning.y))

    while True:
        print('You are in %s' % positioning.predict_location(clf))