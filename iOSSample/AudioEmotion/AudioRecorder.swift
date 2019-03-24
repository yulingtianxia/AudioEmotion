//
//  RecordAudio.swift
//  AudioEmotion
//
//  Created by 杨萧玉 on 2019/3/24.
//  Copyright © 2019 杨萧玉. All rights reserved.
//

import UIKit
import AVFoundation

class AudioRecorder {
    
    let audioURL = { () -> URL in
        let paths = FileManager.default.urls(for: .documentDirectory, in: .userDomainMask)
        let documentsDirectory = paths[0]
        return documentsDirectory.appendingPathComponent("voice.wav")
    }()
    
    let recorder: AVAudioRecorder
    
    init?() {
        let recordSetting = [AVSampleRateKey: 16000.0,
                             AVFormatIDKey: kAudioFormatLinearPCM,
                             AVLinearPCMBitDepthKey: 16,
                             AVNumberOfChannelsKey: 1] as [String : Any]
        do {
            recorder = try AVAudioRecorder(url: audioURL, settings: recordSetting)
        } catch {
            print("recorder creation failed:\(error)")
            return nil
        }
    }
    
    func start() -> Bool {
        do {
            if recorder.prepareToRecord() {
                try AVAudioSession.sharedInstance().setCategory(.playAndRecord, mode: .default)
                try AVAudioSession.sharedInstance().setActive(true)
                return recorder.record()
            }
        } catch {
            print("record failed:\(error.localizedDescription)")
        }
        return false
    }
    
    func stop() -> URL? {
        if recorder.isRecording {
            recorder.stop()
            return self.audioURL
        }
        return nil
    }
}
